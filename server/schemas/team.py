from pydantic import BaseModel, constr


# All Shared properties for a team
class TeamBase(BaseModel):
    name: constr(min_length=2, max_length=200)
    country: str


# All shared properties for a team in DB
class TeamInDBBase(TeamBase):
    id: int

    class Config:
        orm_mode = True


class TeamInDB(TeamInDBBase):
    pass
