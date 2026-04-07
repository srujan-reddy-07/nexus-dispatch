import random
from typing import Tuple, List
from .models import Action, Observation, Emergency, ResponseUnit, EnvState

TASK_CONFIGS = {
    "easy_dispatch": {"n_calls": 1, "n_units": 2, "max_steps": 5},
    "medium_dispatch": {"n_calls": 3, "n_units": 2, "max_steps": 10},
    "hard_dispatch": {"n_calls": 5, "n_units": 2, "max_steps": 15},
}

EMERGENCY_TYPES = ["Medical", "Fire", "Police", "Rescue"]

class NexusEnv:
    def __init__(self):
        self.current_task = "easy_dispatch"
        self.current_calls: List[Emergency] = []
        self.step_count = 0
        self.max_steps = 5
        self.total_reward = 0.0
        self.done = False

    def _make_calls(self, n: int) -> List[Emergency]:
        return [
            Emergency(
                id=f"call_{i:03d}",
                type=random.choice(EMERGENCY_TYPES),
                severity=random.randint(1, 5),
                location=[round(random.uniform(-90, 90), 4), round(random.uniform(-180, 180), 4)]
            )
            for i in range(1, n + 1)
        ]

    def _make_units(self, n: int) -> List[ResponseUnit]:
        types = ["Ambulance", "FireTruck", "PoliceUnit", "RescueTeam"]
        return [
            ResponseUnit(
                id=f"unit_{i:03d}",
                type=types[(i - 1) % len(types)],
                status="Available",
                location=[0.0, 0.0]
            )
            for i in range(1, n + 1)
        ]

    def reset(self, task: str = "easy_dispatch") -> Observation:
        config = TASK_CONFIGS.get(task, TASK_CONFIGS["easy_dispatch"])
        self.current_task = task
        self.step_count = 0
        self.max_steps = config["max_steps"]
        self.total_reward = 0.0
        self.done = False
        self.current_calls = self._make_calls(config["n_calls"])
        self._units = self._make_units(config["n_units"])
        return Observation(calls=self.current_calls, units=self._units)

    def step(self, action: Action) -> Tuple[Observation, float, bool, dict]:
        self.step_count += 1
        reward = 0.0
        info = {"status": "success", "step": self.step_count}

        if action.type == "DISPATCH" and action.unit_id and action.call_id:
            matched = next((c for c in self.current_calls if c.id == action.call_id), None)
            if matched:
                reward = matched.severity / 5.0
                self.current_calls = [c for c in self.current_calls if c.id != action.call_id]
            else:
                info["status"] = "invalid_call"
        elif action.type == "WAIT":
            reward = 0.0
        else:
            info["status"] = "invalid_action"

        self.total_reward += reward
        self.done = (not self.current_calls) or (self.step_count >= self.max_steps)

        obs = Observation(calls=self.current_calls, units=self._units)
        return obs, reward, self.done, info

    def state(self) -> EnvState:
        return EnvState(
            task=self.current_task,
            step_count=self.step_count,
            active_calls=len(self.current_calls),
            total_reward=self.total_reward,
            done=self.done
        )
