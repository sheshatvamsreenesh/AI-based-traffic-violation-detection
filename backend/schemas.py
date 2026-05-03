from pydantic import BaseModel
from typing import List
from enum import Enum

class ViolationType(str, Enum):
    WRONG_LANE = "wrong_lane"
    NO_HELMET = "no_helmet"
    SIGNAL_JUMP = "signal_jump"
    TRIPLE_RIDING = "triple_riding"

class ViolationCreate(BaseModel):
    type: ViolationType
    timestamp: str
    confidence: float
    image_path: str

class AIResult(BaseModel):
    video_id: str
    violations: List[ViolationCreate]