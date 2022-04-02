import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy_utils import ChoiceType

from server.database import Base


class EventType(int, enum.Enum):
    start = 1
    goal = 2
    half_time = 3
    stoppage_time = 4
    substitution = 5
    warning = 6
    end = 7


class MatchEvent(Base):
    __tablename__ = 'match_event'
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
    time = Column(DateTime, nullable=False)
    event_type = Column(ChoiceType(EventType, impl=Integer()))
    string_value = Column(String, nullable=True)
    integer_value = Column(Integer, nullable=True)
