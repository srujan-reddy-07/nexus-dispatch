from pydantic import BaseModel
from typing import List, Optional

class Action(BaseModel):
    type: str
    unit_id: Optional[str] = None
    call_id: Optional[str] = None

class Emergency(BaseModel):
    id: str
    type: str
    severity: int
    location: List[float]

class ResponseUnit(BaseModel):
    id: str
    type: str
    status: str
    location: List[float]

class Observation(BaseModel):
    calls: List[Emergency] = []
    units: List[ResponseUnit] = []

class EnvState(BaseModel):
    task: str
    step_count: int
    active_calls: int
    total_reward: float
    done: bool
