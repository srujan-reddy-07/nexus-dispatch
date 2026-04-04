import random
from typing import Tuple, Dict, List
from .models import Action, Observation, Emergency, ResponseUnit

class NexusEnv:
    def __init__(self):
        self.state = "initial"
        self.current_calls: List[Emergency] = [] 
        
    def step(self, action: Action) -> Tuple[Observation, float, bool, dict]:
        obs = Observation()
        reward = 1.0
        done = False
        info = {"status": "success"}
        return obs, reward, done, info