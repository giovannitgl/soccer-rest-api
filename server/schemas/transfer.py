from datetime import datetime

from pydantic import BaseModel, constr, condecimal


# All Shared properties for a transfer
class TransferBase(BaseModel):
    date: datetime
    value: condecimal(max_digits=10, decimal_places=2)
    name: constr(min_length=2, max_length=200)


# All shared properties for a transfer in DB
class TransferInDBBase(TransferBase):
    id: int
    player_id: int
    origin_team_id: int
    destination_team_id: int

    class Config:
        orm_mode = True


class TransferInDB(TransferBase):
    pass
