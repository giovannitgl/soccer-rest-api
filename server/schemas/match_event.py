from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

from server.models.match_event import EventType


# All Shared properties for a match event
class MatchEventBase(BaseModel):
    time: datetime
    event_type: EventType
    string_value: Optional[str]
    integer_value: Optional[int]


# Properties for creating a match event
class MatchEventCreate(MatchEventBase):
    match_id: int


# Properties for update a match event
class MatchEventUpdate(BaseModel):
    time: datetime
    string_value: Optional[str]
    integer_value: Optional[int]


# All shared properties for a match event in DB
class MatchEventInDBBase(MatchEventBase):
    id: int
    match_id: int

    class Config:
        orm_mode = True


class MatchEventInDB(MatchEventInDBBase):
    pass


# Properties for get MatchEvent
class MatchEvent(MatchEventInDB):
    pass
