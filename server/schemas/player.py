from datetime import datetime

from pydantic import BaseModel, constr


# All Shared properties for player
class PlayerBase(BaseModel):
    first_name: constr(min_length=2, max_length=60)
    last_name: constr(min_length=2, max_length=60)
    birth_date: datetime
    country: str


# All shared properties for a player in DB
class PlayerInDBBase(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True


class PlayerInDB(PlayerBase):
    pass
