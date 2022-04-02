from datetime import date, datetime

from pydantic import BaseModel, constr, condecimal


# All Shared properties for a match
class MatchBase(BaseModel):
    start_time: datetime


# Properties for creating a match
class MatchCreate(MatchBase):
    team_1_id: int
    team_2_id: int


# Properties used internally for creating a match.
class MatchCreateInternal(MatchCreate):
    tournament_id: int


# Properties for update a match
class MatchUpdate(BaseModel):
    start_time: datetime


# All shared properties for a match in DB
class MatchInDBBase(MatchBase):
    id: int
    tournament_id: int
    team_1_id: int
    team_2_id: int

    class Config:
        orm_mode = True


class MatchInDB(MatchInDBBase):
    pass


# Properties for get Match
class Match(MatchInDB):
    pass
