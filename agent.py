# agent.py
import numpy as np
from typing import Optional, List, Tuple
from pydantic import BaseModel
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
# Observation space: [speed, progress, angle_diff, gradient_x, gradient_y]
OBS_DIM = 5
# Action space: 0=noop, 1=accelerate, 2=brake, 3=turn_left, 4=turn_right
ACTION_DIM = 5

class GameState(BaseModel):
    speed: Optional[float] = 0.0
    progress: Optional[float] = 0.0
    angle_diff: Optional[float] = 0.0
    gradient_x: Optional[float] = 0.0
    gradient_y: Optional[float] = 0.0

class PPONetwork(nn.Module):
    """
    Actor-Critic network for PPO.
    Shared feature extractor with separate heads for policy and value.
    """
    def __init__(self, obs_dim: int, action_dim: int, hidden_size: int = 64):
        super(PPONetwork, self).__init__()
        
        # Shared feature extractor
        self.feature = nn.Sequential(
            nn.Linear(obs_dim, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh()
        )
        
        # Actor (policy) head
        self.actor = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, action_dim)
        )
        
        # Critic (value) head
        self.critic = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        )
    
    def forward(self, obs):
        """Forward pass through the network."""
        features = self.feature(obs)
        action_logits = self.actor(features)
        value = self.critic(features)
        return action_logits, value
    
    def get_action_and_value(self, obs, action=None):
        """
        Get action, log probability, entropy, and value estimate.
        
        Args:
            obs: Observation tensor
            action: Optional action (if None, samples from policy)
            
        Returns:
            action, log_prob, entropy, value
        """
        action_logits, value = self.forward(obs)
        probs = Categorical(logits=action_logits)
        if action is None:
            action = probs.sample()
        return action, probs.log_prob(action), probs.entropy(), value.squeeze()

class Agent:
    """
    Agent with custom PPO training loop that works with websocket observations.
    Collects experiences from websocket and trains periodically.
    """
    def __init__(
        self, 
        model_path: Optional[str] = None, 
        training_mode: bool = True,
        n_steps: int = 1000,
        batch_size: int = 64,
        n_epochs: int = 10,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        clip_eps: float = 0.2,
        learning_rate: float = 3e-4,
        ent_coef: float = 0.01,
        vf_coef: float = 0.5,
        max_grad_norm: float = 0.5
    ):
        """
        Initialize the agent.
        
        Args:
            model_path: Path to save/load the model
            training_mode: If True, collects experiences and trains
            n_steps: Number of steps to collect before training
            batch_size: Batch size for training
            n_epochs: Number of epochs to train on collected data
            gamma: Discount factor
            gae_lambda: GAE lambda parameter
            clip_eps: PPO clip epsilon
            learning_rate: Learning rate
            ent_coef: Entropy coefficient
            vf_coef: Value function loss coefficient
            max_grad_norm: Maximum gradient norm for clipping
        """
        self.model_path = model_path or "mariokart_ppo_model"
        self.training_mode = training_mode
        
        # Hyperparameters
        self.n_steps = n_steps
        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_eps = clip_eps
        self.ent_coef = ent_coef
        self.vf_coef = vf_coef
        self.max_grad_norm = max_grad_norm
        
        # Network
        obs_dim = OBS_DIM
        action_dim = ACTION_DIM
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.network = PPONetwork(obs_dim, action_dim).to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=learning_rate)
        
        # Experience buffers
        self.observations: List[np.ndarray] = []
        self.actions: List[int] = []
        self.rewards: List[float] = []
        self.dones: List[bool] = []
        self.log_probs: List[float] = []
        self.values: List[float] = []
        
        # State tracking
        self.step_count = 0
        self.total_timesteps = 0
        self.prev_progress = 0.0
        
        # Load model if exists
        if os.path.exists(f"{self.model_path}.pt"):
            print(f"Loading model from {self.model_path}.pt")
            self.network.load_state_dict(torch.load(f"{self.model_path}.pt", map_location=self.device))
            self.network.eval()
        else:
            print("Creating new PPO model")

    def _state_to_obs(self, obs_dict: dict) -> np.ndarray:
        """
        Convert observation dictionary to observation array.
        
        Observation format: [speed, progress, angle_diff, gradient_x, gradient_y]
        """
        def to_float(value, default=0.0):
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        obs = np.array([
            to_float(obs_dict.get("speed", 0.0)),
            to_float(obs_dict.get("progress", 0.0)),
            to_float(obs_dict.get("angle_diff", 0.0)),
            to_float(obs_dict.get("gradient_x", 0.0)),
            to_float(obs_dict.get("gradient_y", 0.0))
        ], dtype=np.float32)
        
        return obs

    def _calculate_reward(self, state: dict, action: int) -> float:
        """
        Calculate reward based on state and action.
        
        Reward components:
        - Progress: positive reward for making progress
        - Speed: positive reward for maintaining speed
        - Angle alignment: negative reward for large angle differences
        - Action efficiency: small penalty for unnecessary actions
        """
        # Convert values to float (handle string values from websocket)
        def to_float(value, default=0.0):
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        progress = to_float(state.get("progress", 0.0))
        speed = to_float(state.get("speed", 0.0))
        angle_diff = to_float(state.get("angle_diff", 0.0))
        
        # Reward for progress (main objective)
        progress_reward = (progress - self.prev_progress) * 10.0
        
        # Reward for maintaining speed
        speed_reward = speed * 0.1
        
        # Penalty for being misaligned (large angle difference)
        angle_penalty = -abs(angle_diff) * 0.5
        
        # Small penalty for doing nothing when action is needed
        action_penalty = 0.0
        if action == 0 and abs(angle_diff) > 0.1:
            action_penalty = -0.01
        
        total_reward = progress_reward + speed_reward + angle_penalty + action_penalty
        self.prev_progress = progress
        return total_reward

    def collect_step(self, obs: dict, done: bool = False) -> int:
        """
        Collect one step of experience and return action to take.
        Call this when receiving a new observation from websocket.
        
        Args:
            obs: Current observation as a dictionary
            done: Whether episode is done
            
        Returns:
            Action to take (0-4)
        """
        # Convert dict to numpy array observation
        obs_array = self._state_to_obs(obs)
        obs_tensor = torch.FloatTensor(obs_array).unsqueeze(0).to(self.device)
        
        # Get action from network
        with torch.no_grad():
            action, log_prob, entropy, value = self.network.get_action_and_value(obs_tensor)
            action = action.item()
            log_prob = log_prob.item()
            value = value.item()
        
        # Calculate reward if training
        reward = self._calculate_reward(obs, action) if self.training_mode else 0.0
        
        # Store experience
        if self.training_mode:
            self.observations.append(obs_array)
            self.actions.append(action)
            self.rewards.append(reward)
            self.dones.append(done)
            self.log_probs.append(log_prob)
            self.values.append(value)
            
            self.step_count += 1
            self.total_timesteps += 1
            
            # Train when we have enough steps
            if self.step_count >= self.n_steps:
                self._train_on_collected_experiences()
                self._clear_experience_buffer()
        
        return action

    def _compute_gae(self, rewards: np.ndarray, values: np.ndarray, dones: np.ndarray, 
                     next_value: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute Generalized Advantage Estimation (GAE).
        
        Args:
            rewards: Array of rewards
            values: Array of value estimates
            dones: Array of done flags
            next_value: Value estimate for the next state
            
        Returns:
            advantages: GAE advantages
            returns: Discounted returns
        """
        advantages = np.zeros_like(rewards, dtype=np.float32)
        last_gae = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_non_terminal = 1.0 - dones[t]
                next_value_t = next_value
            else:
                next_non_terminal = 1.0 - dones[t]
                next_value_t = values[t + 1]
            
            delta = rewards[t] + self.gamma * next_value_t * next_non_terminal - values[t]
            advantages[t] = last_gae = delta + self.gamma * self.gae_lambda * next_non_terminal * last_gae
        
        returns = advantages + values
        return advantages, returns

    def _train_on_collected_experiences(self):
        """Train the model on collected experiences using PPO."""
       
        print(f"\nTraining on {len(self.observations)} experiences (total timesteps: {self.total_timesteps})...")
        
        # Convert to numpy arrays
        obs_array = np.array(self.observations, dtype=np.float32)
        actions_array = np.array(self.actions, dtype=np.int64)
        rewards_array = np.array(self.rewards, dtype=np.float32)
        dones_array = np.array(self.dones, dtype=np.float32)
        old_log_probs_array = np.array(self.log_probs, dtype=np.float32)
        values_array = np.array(self.values, dtype=np.float32)
        
        # Compute next value (for GAE)
        if len(obs_array) > 0:
            last_obs = torch.FloatTensor(obs_array[-1]).unsqueeze(0).to(self.device)
            with torch.no_grad():
                _, _, _, next_value = self.network.get_action_and_value(last_obs)
                next_value = next_value.item()
        else:
            next_value = 0.0
        
        # Compute advantages and returns
        advantages, returns = self._compute_gae(rewards_array, values_array, dones_array, next_value)
        
        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # Convert to tensors
        obs_tensor = torch.FloatTensor(obs_array).to(self.device)
        actions_tensor = torch.LongTensor(actions_array).to(self.device)
        old_log_probs_tensor = torch.FloatTensor(old_log_probs_array).to(self.device)
        advantages_tensor = torch.FloatTensor(advantages).to(self.device)
        returns_tensor = torch.FloatTensor(returns).to(self.device)
        
        # Training loop
        indices = np.arange(len(obs_array))
        total_policy_loss = 0
        total_value_loss = 0
        total_entropy = 0
        n_updates = 0
        
        for epoch in range(self.n_epochs):
            np.random.shuffle(indices)
            
            for start in range(0, len(indices), self.batch_size):
                end = start + self.batch_size
                batch_indices = indices[start:end]
                
                # Get batch
                batch_obs = obs_tensor[batch_indices]
                batch_actions = actions_tensor[batch_indices]
                batch_old_log_probs = old_log_probs_tensor[batch_indices]
                batch_advantages = advantages_tensor[batch_indices]
                batch_returns = returns_tensor[batch_indices]
                
                # Forward pass
                _, new_log_probs, entropy, new_values = self.network.get_action_and_value(
                    batch_obs, batch_actions
                )
                
                # Compute policy loss (PPO clipped objective)
                ratio = torch.exp(new_log_probs - batch_old_log_probs)
                policy_loss_1 = batch_advantages * ratio
                policy_loss_2 = batch_advantages * torch.clamp(
                    ratio, 1 - self.clip_eps, 1 + self.clip_eps
                )
                policy_loss = -torch.min(policy_loss_1, policy_loss_2).mean()
                
                # Compute value loss
                value_loss = nn.functional.mse_loss(new_values.squeeze(), batch_returns)
                
                # Compute entropy
                entropy_loss = entropy.mean()
                
                # Total loss
                loss = policy_loss + self.vf_coef * value_loss - self.ent_coef * entropy_loss
                
                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
                self.optimizer.step()
                
                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += entropy_loss.item()
                n_updates += 1
        
        avg_policy_loss = total_policy_loss / n_updates if n_updates > 0 else 0
        avg_value_loss = total_value_loss / n_updates if n_updates > 0 else 0
        avg_entropy = total_entropy / n_updates if n_updates > 0 else 0
        
        print(f"  Policy Loss: {avg_policy_loss:.4f}, Value Loss: {avg_value_loss:.4f}, Entropy: {avg_entropy:.4f}")
        
        # Save model
        self.save()

    def _clear_experience_buffer(self):
        """Clear the experience buffer after training."""
        self.observations = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.log_probs = []
        self.values = []
        self.step_count = 0

    def act(self, state: GameState, deterministic: bool = True) -> int:
        """
        Get action from the trained model (inference only, no experience collection).
        Use collect_step() during training instead.
        
        Args:
            state: Current game state
            deterministic: If True, use the most likely action. If False, sample from policy.
            
        Returns:
            Action to take (0-4)
        """
        obs = self._state_to_obs(state)
        obs_tensor = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            if deterministic:
                # Use the most likely action
                action_logits, _ = self.network(obs_tensor)
                action = torch.argmax(action_logits, dim=1).item()
            else:
                # Sample from policy
                action, _, _, _ = self.network.get_action_and_value(obs_tensor)
                action = action.item()
        
        return action

    def _seed_policy(self, state: GameState) -> int:
        """
        Fallback seed policy (rule-based) when model is not trained.
        This is the original angle-based agent logic.
        """
        # Priority 1: Get unstuck
        if abs(state.speed) < 0.01:
            return 1  # Accelerate
        
        # Priority 2: Angle-based steering
        if abs(state.angle_diff) > 2.0:  # Sharp turn
            return 3 if state.angle_diff > 0 else 4
        elif abs(state.angle_diff) > 1.0:  # Moderate turn
            return 3 if state.angle_diff > 0 else 4
        elif abs(state.angle_diff) > 0.3:  # Slight turn
            return 3 if state.angle_diff > 0 else 4
        else:
            # Well aligned - accelerate
            return 1

    def save(self, path: Optional[str] = None):
        """Save the model."""
        path = path or self.model_path
        torch.save(self.network.state_dict(), f"{path}.pt")
        print(f"Model saved to {path}.pt")

    def load(self, path: Optional[str] = None):
        """Load the model."""
        path = path or self.model_path
        if os.path.exists(f"{path}.pt"):
            self.network.load_state_dict(torch.load(f"{path}.pt", map_location=self.device))
            self.network.eval()
            print(f"Model loaded from {path}.pt")
