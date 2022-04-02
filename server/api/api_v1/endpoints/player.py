from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import cruds, schemas
from server.api import deps
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


@router.get("/", response_model=List[schemas.Player])
async def list_players(
    db: Session = Depends(deps.get_db),
    skip: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT
) -> Any:
    """
    List players
    """
    return cruds.player.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Player)
async def list_player(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    """
    List players.
    """
    player = cruds.player.get(db, id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.post("/", response_model=schemas.Player)
async def create_player(
    *,
    db: Session = Depends(deps.get_db),
    player_in: schemas.PlayerCreate
) -> Any:
    """
    Create new player.
    """
    player = cruds.player.create(db=db, obj_in=player_in)
    return player


@router.put("/{id}", response_model=schemas.Player)
async def update_player(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    player_in: schemas.PlayerUpdate
) -> Any:
    """
    Update a player.
    """
    player = cruds.player.get(db=db, id=id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player = cruds.player.update(db=db, db_obj=player, obj_in=player_in)
    return player


@router.delete("/{id}", response_model=schemas.Player)
async def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a player.
    """
    player = cruds.player.get(db=db, id=id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player = cruds.player.remove(db=db, id=id)
    return player
