from datetime import date
from typing import Optional

from pydantic import BaseModel, constr


# All Shared properties for player
class PlayerBase(BaseModel):
    first_name: constr(min_length=2, max_length=60)
    last_name: constr(min_length=2, max_length=60)
    birth_date: date
    country: str


# Properties received on create
class PlayerCreate(PlayerBase):
    team_id: Optional[int]


# Properties received on update
class PlayerUpdate(PlayerBase):
    pass


# All shared properties for a player in DB
class PlayerInDBBase(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True


class PlayerInDB(PlayerInDBBase):
    pass


# Properties for getting player
class Player(PlayerInDB):
    pass
