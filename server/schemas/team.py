from pydantic import BaseModel, constr


# All Shared properties for a team
class TeamBase(BaseModel):
    name: constr(min_length=2, max_length=200)
    country: str


# Properties for creating a team
class TeamCreate(TeamBase):
    pass


# Properties for updating a team
class TeamUpdate(TeamBase):
    pass


# All shared properties for a team in DB
class TeamInDBBase(TeamBase):
    id: int

    class Config:
        orm_mode = True


class TeamInDB(TeamInDBBase):
    pass


# Properties for get team
class Team(TeamInDB):
    pass
