
from pydantic import BaseModel
from typing import List, Optional, Dict

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
    assigned_to: Optional[str] = None

class Observation(BaseModel):
    calls: List[Emergency] = []
    units: List[ResponseUnit] = []
    distances: Optional[Dict[str, Dict[str, float]]] = None

class EnvState(BaseModel):
    task: str
    step_count: int
    active_calls: int
    total_reward: float
    done: bool
    lives_saved: int = 0
    avg_response_time: float = 0.0
    specialization_accuracy: float = 0.0
