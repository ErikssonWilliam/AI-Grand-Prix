# my_agent.py
import numpy as np
from typing import Optional
from pydantic import BaseModel

class GameState(BaseModel):
    speed: Optional[float] = 0.0
    progress: Optional[float] = 0.0
    angle_diff: Optional[float] = 0.0
    gradient_x: Optional[float] = 0.0
    gradient_y: Optional[float] = 0.0

class Agent:
    def __init__(self):
        self.step_count = 0
        print("Angle-based agent (like built-in AI)")

    def seed_policy(self, state: GameState) -> int:
        self.step_count += 1
        
        print(f"ANGLE_AGENT - Speed: {state.speed:.3f}, AngleDiff: {state.angle_diff:.3f}")
        
        # Priority 1: Get unstuck
        if abs(state.speed) < 0.01 and self.step_count > 10:
            if self.step_count % 8 < 6:
                return 1  # Accelerate
            else:
                return 3 if state.angle_diff > 0 else 4  # Turn based on angle
        
        # Priority 2: Angle-based steering (like built-in AI)
        # Convert angle_diff to turn intensity
        if abs(state.angle_diff) > 2.0:  # ~115 degrees - sharp turn
            if state.angle_diff > 0:
                return 3  # Turn left hard
            else:
                return 4  # Turn right hard
        elif abs(state.angle_diff) > 1.0:  # ~57 degrees - moderate turn
            if state.angle_diff > 0:
                return 3  # Turn left
            else:
                return 4  # Turn right
        elif abs(state.angle_diff) > 0.3:  # ~17 degrees - slight turn
            # 70% chance to turn, 30% to accelerate
            if np.random.rand() < 0.7:
                return 3 if state.angle_diff > 0 else 4
            else:
                return 1
        else:
            # Well aligned - accelerate!
            return 1

    def act(self, state: GameState) -> int:
        return self.seed_policy(state)