from pydantic import BaseModel
from typing import List, Optional

class Action(BaseModel):
    dispatch_unit_id: str
    call_id: str

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