from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import cruds, schemas
from server.api import deps
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


@router.get("/", response_model=List[schemas.Transfer])
async def list_transfers(
    db: Session = Depends(deps.get_db),
    skip: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT
) -> Any:
    """
    L
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return cruds.transfer.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Transfer)
async def list_transfer(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    """
    List transfers.
    """
    transfer = cruds.transfer.get(db, id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    return transfer


@router.post("/", response_model=schemas.Transfer)
async def create_transfer(
    *,
    db: Session = Depends(deps.get_db),
    transfer_in: schemas.TransferCreate
) -> Any:
    """
    Create new transfer.
    """
    player = cruds.player.get(db, transfer_in.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="User not found")
    internal_transfer = schemas.TransferCreateInternal(**transfer_in.__dict__, origin_team_id=player.team_id)
    transfer = cruds.transfer.create(db=db, obj_in=internal_transfer)
    return transfer


@router.put("/{id}", response_model=schemas.Transfer)
async def update_transfer(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    transfer_in: schemas.TransferUpdate
) -> Any:
    """
    Update a transfer.
    """
    transfer = cruds.transfer.get(db=db, id=id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    transfer = cruds.transfer.update(db=db, db_obj=transfer, obj_in=transfer_in)
    return transfer


@router.delete("/{id}", response_model=schemas.Transfer)
async def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a transfer.
    """
    transfer = cruds.transfer.get(db=db, id=id)
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer not found")
    transfer = cruds.transfer.remove(db=db, id=id)
    return transfer
