from datetime import date

from pydantic import BaseModel, constr, condecimal


# All Shared properties for a transfer
class TransferBase(BaseModel):
    date: date
    value: condecimal(max_digits=10, decimal_places=2)
    player_id: int
    destination_team_id: int


# Properties for creating a transfer
class TransferCreate(TransferBase):
    pass


# Properties for creating a transfer
class TransferCreateInternal(TransferBase):
    origin_team_id: int


# Properties for update a transfer
class TransferUpdate(BaseModel):
    value: condecimal(max_digits=10, decimal_places=2)


# All shared properties for a transfer in DB
class TransferInDBBase(TransferBase):
    id: int
    origin_team_id: int

    class Config:
        orm_mode = True


class TransferInDB(TransferInDBBase):
    pass


# Properties for get Transfer
class Transfer(TransferInDB):
    pass
