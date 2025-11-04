# my_agent.py
import numpy as np
from typing import Optional
from pydantic import BaseModel

# Update GameState to include speed
class GameState(BaseModel):
    GameFrame: int
    PlayerHealth: int
    angle_to_next: Optional[float] = 0.0
    off_track: Optional[bool] = False
    speed: Optional[float] = 0.0  # Add speed for stuck detection

class Agent:
    def __init__(self):
        self.prev_angle_to_next = 0
        self.W = np.random.randn() * 0.1
        self.learning_rate = 0.01
        self.noise_std = 0.05
        print("Agent instance created. Loading model...")

    def seed_policy(self, state: GameState) -> int:
        """
        Enhanced baseline driving logic with stuck detection and sharper steering.
        Returns an action 0-4.
        """
        # Detect if stuck (very slow speed)
        is_stuck = abs(state.speed) < 0.1 if state.speed is not None else False
        
        # Recovery strategy when stuck
        if is_stuck:
            # Alternate turning directions to get unstuck
            if self.prev_angle_to_next > 0:
                return 4  # Turn right
            else:
                return 3  # Turn left
        
        # If off track, prioritize getting back on track
        if state.off_track:
            return 3 if state.angle_to_next > 0 else 4
        
        # Normal driving based on turn sharpness
        if abs(state.angle_to_next) > 1.0:  # Very sharp turn
            return 2  # Brake hard
        elif abs(state.angle_to_next) > 0.5:  # Sharp turn
            # 30% chance to brake during sharp turns
            return 2 if np.random.rand() < 0.3 else (3 if state.angle_to_next > 0 else 4)
        elif abs(state.angle_to_next) > 0.2:  # Moderate turn
            return 3 if state.angle_to_next > 0 else 4
        else:  # Straight path - accelerate
            return 1

    def act(self, state: GameState) -> int:
        """
        This method receives the current game state and should return an action.
        """
        action = self.seed_policy(state)

        # 10% chance to explore random actions
        if np.random.rand() < 0.1:
            action = np.random.choice([0, 1, 2, 3, 4])

        self.prev_angle_to_next = state.angle_to_next

        return action