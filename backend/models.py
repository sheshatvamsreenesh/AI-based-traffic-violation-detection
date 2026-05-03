from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from database import Base
import enum

class ViolationType(enum.Enum):
    WRONG_LANE = "wrong_lane"
    NO_HELMET = "no_helmet"
    SIGNAL_JUMP = "signal_jump"
    TRIPLE_RIDING = "triple_riding"

class Video(Base):
    __tablename__ = "videos"

    id = Column(String(50), primary_key=True)
    file_path = Column(String(255))
    status = Column(String(20))

class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(50), ForeignKey("videos.id"))
    type = Column(Enum(ViolationType))
    timestamp = Column(String(20))
    confidence = Column(Float)
    image_path = Column(String(255))