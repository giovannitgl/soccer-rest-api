from datetime import date

from pydantic import BaseModel, constr


# All Shared properties for a tournament
class TournamentBase(BaseModel):
    name: constr(min_length=2, max_length=200)
    start_day: date


# Properties for creating a tournament
class TournamentCreate(TournamentBase):
    pass


# Properties for updating a tournament
class TournamentUpdate(TournamentBase):
    pass


# Properties for adding team in tournament
class TournamentAddTeam(BaseModel):
    team_id: int


# All shared properties for a tournament in DB
class TournamentInDBBase(TournamentBase):
    id: int

    class Config:
        orm_mode = True


class TournamentInDB(TournamentInDBBase):
    pass


# Properties for get tournament
class Tournament(TournamentInDB):
    pass
