
import random
import math
from typing import Tuple, List, Dict
from .models import Action, Observation, Emergency, ResponseUnit, EnvState

TASK_CONFIGS = {
    "easy_dispatch": {"n_calls": 1, "n_units": 2, "max_steps": 10},
    "medium_dispatch": {"n_calls": 3, "n_units": 4, "max_steps": 20},
    "hard_dispatch": {"n_calls": 6, "n_units": 4, "max_steps": 30},
}

EMERGENCY_TYPES = ["Medical", "Fire", "Police", "Rescue"]
TYPE_MATCHING = {
    "Medical": ["Ambulance", "RescueTeam"],
    "Fire": ["FireTruck"],
    "Police": ["PoliceUnit"],
    "Rescue": ["RescueTeam", "FireTruck"]
}

class NexusEnv:
    def __init__(self):
        self.current_task = "easy_dispatch"
        self.current_calls: List[Emergency] = []
        self._units: List[ResponseUnit] = []
        self.step_count = 0
        self.max_steps = 10
        self.total_reward = 0.0
        self.done = False
        self.lives_saved = 0
        self.total_response_dist = 0.0
        self.match_count = 0

    def _calculate_distance(self, loc1, loc2):
        return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    def reset(self, task: str = "easy_dispatch") -> Observation:
        config = TASK_CONFIGS.get(task, TASK_CONFIGS["easy_dispatch"])
        self.current_task, self.step_count, self.max_steps = task, 0, config["max_steps"]
        self.total_reward, self.done, self.lives_saved, self.total_response_dist, self.match_count = 0.0, False, 0, 0.0, 0
        self.current_calls = [Emergency(id=f"CALL-{i:03d}", type=random.choice(EMERGENCY_TYPES), severity=random.randint(1, 5), location=[random.uniform(0, 100), random.uniform(0, 100)]) for i in range(1, config["n_calls"] + 1)]
        self._units = [ResponseUnit(id=f"UNIT-{i:03d}", type=["Ambulance", "FireTruck", "PoliceUnit", "RescueTeam"][(i - 1) % 4], status="Available", location=[random.uniform(0, 100), random.uniform(0, 100)]) for i in range(1, config["n_units"] + 1)]
        return self._get_observation()

    def _get_observation(self):
        dist_map = {u.id: {c.id: self._calculate_distance(u.location, c.location) for c in self.current_calls} for u in self._units}
        return Observation(calls=self.current_calls, units=self._units, distances=dist_map)

    def step(self, action: Action):
        self.step_count += 1
        reward, info = 0.0, {"status": "success"}
        if action.type == "DISPATCH" and action.unit_id and action.call_id:
            unit = next((u for u in self._units if u.id == action.unit_id), None)
            call = next((c for c in self.current_calls if c.id == action.call_id), None)
            if unit and call and unit.status == "Available":
                dist = self._calculate_distance(unit.location, call.location)
                is_match = unit.type in TYPE_MATCHING.get(call.type, [])
                reward = (call.severity / 5.0) * (1.0 if is_match else 0.5) * max(0.2, 1.0 - (dist / 142.0))
                unit.location, self.lives_saved, self.total_response_dist = call.location, self.lives_saved + 1, self.total_response_dist + dist
                if is_match: self.match_count += 1
                self.current_calls = [c for c in self.current_calls if c.id != call.id]
        self.total_reward += reward
        self.done = (not self.current_calls) or (self.step_count >= self.max_steps)
        return self._get_observation(), reward, self.done, info

    def state(self):
        acc = (self.match_count / self.lives_saved) if self.lives_saved > 0 else 0.0
        avg_d = (self.total_response_dist / self.lives_saved) if self.lives_saved > 0 else 0.0
        return EnvState(task=self.current_task, step_count=self.step_count, active_calls=len(self.current_calls), total_reward=self.total_reward, done=self.done, lives_saved=self.lives_saved, avg_response_time=avg_d, specialization_accuracy=acc)
