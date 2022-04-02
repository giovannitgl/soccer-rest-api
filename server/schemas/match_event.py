from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from server.models.match_event import EventType


# All Shared properties for a match event
class MatchEventBase(BaseModel):
    time: datetime


# Properties for creating a match event
class MatchEventCreate(MatchEventBase):
    pass


# Information for registering start event
class MatchEventStartCreate(MatchEventCreate):
    pass


# Information for registering end event
class MatchEventEndCreate(MatchEventCreate):
    pass


# Information for registering goal event
class MatchEventGoalCreate(MatchEventCreate):
    player_id: int
    team_id: int


# Information for registering half_time event
class MatchEventHalfTimeCreate(MatchEventCreate):
    pass


# Information for registering stoppage event
class MatchEventStoppageCreate(MatchEventCreate):
    minutes: int


# Information for registering substitution event
class MatchEventSubstitutionCreate(MatchEventCreate):
    player_out: int
    player_in: int


# Information for registering warning event
class MatchEventWarningCreate(MatchEventCreate):
    player_id: int
    warning_type: str


# Internal properties when creating a match
class MatchEventCreateInternal(MatchEventBase):
    match_id: int
    event_type: EventType
    player_id: Optional[int]
    string_value: Optional[str]
    integer_value: Optional[int]


# Information for updating match event
class MatchEventUpdate(MatchEventBase):
    pass


# All shared properties for a match event in DB
class MatchEventInDBBase(MatchEventBase):
    id: int
    match_id: int
    event_type: EventType
    string_value: Optional[str]
    integer_value: Optional[int]

    class Config:
        orm_mode = True


class MatchEventInDB(MatchEventInDBBase):
    pass


# Properties for get MatchEvent
class MatchEvent(MatchEventInDB):
    pass
