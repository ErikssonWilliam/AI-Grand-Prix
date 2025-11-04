# my_agent.py
import numpy as np
from typing import Optional
from pydantic import BaseModel # Import this to define the state model

# Define the exact same GameState model as in agent_server.py
class GameState(BaseModel):
    GameFrame: int
    PlayerHealth: int
    angle_to_next: Optional[float] = 00
    off_track: Optional[bool] = False

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

        return 1 #Accelerate