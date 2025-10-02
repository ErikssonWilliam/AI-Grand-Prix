# my_agent.py
import numpy as np
from pydantic import BaseModel # Import this to define the state model

# Define the exact same GameState model as in agent_server.py
class GameState(BaseModel):
    speed: float
    dist_to_next: float
    angle_to_next: float
    off_track: bool
    done: bool

# This is the class where the participants will put their logic.
class Agent:
    def __init__(self):
        # This constructor is called once when the server starts.
        # This is the perfect place to load your pre-trained model.
        print("Agent instance created. Loading model...")
        # Example: self.model = torch.load('my_model_weights.pth')
        
    def act(self, state: GameState) -> int:
        """
        This method receives the current game state and should return an action.
        
        Args:
            state: The current GameState object.
            
        Returns:
            An integer representing the chosen action.
            Actions: 0 = none, 1 = accelerate, 2 = brake, 3 = left, 4 = right
        """
        # Example: a simple "smart" agent
        if state.done:
            return 0  # Stop if the race is over

        # If we're off-track, slow down and correct
        if state.off_track:
            if state.angle_to_next < 0:
                return 4  # Turn right
            else:
                return 3  # Turn left

        # If we're far from the next checkpoint, accelerate
        if state.dist_to_next > 20 and state.speed < 15:
            return 1  # Accelerate
            
        # If we are aligned, keep accelerating
        if abs(state.angle_to_next) < 0.1 and state.speed < 25:
             return 1
             
        # Otherwise, take a random action for fun or exploration
        return np.random.choice([0, 1, 2, 3, 4])