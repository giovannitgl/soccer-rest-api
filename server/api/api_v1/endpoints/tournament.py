from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import cruds, schemas
from server.api import deps
from server.api.api_v1.endpoints import match, tournament_team, match_event
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


@router.get("/", response_model=List[schemas.Tournament])
async def list_tournaments(
    db: Session = Depends(deps.get_db),
    skip: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT
) -> Any:
    """
    List tournaments
    """
    return cruds.tournament.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Tournament)
async def list_tournament(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    """
    List tournaments.
    """
    tournament = cruds.tournament.get(db, id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament


@router.post("/", response_model=schemas.Tournament)
async def create_tournament(
    *,
    db: Session = Depends(deps.get_db),
    tournament_in: schemas.TournamentCreate
) -> Any:
    """
    Create new tournament.
    """
    tournament = cruds.tournament.create(db=db, obj_in=tournament_in)
    return tournament


@router.put("/{id}", response_model=schemas.Tournament)
async def update_tournament(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    tournament_in: schemas.TournamentUpdate
) -> Any:
    """
    Update a tournament.
    """
    tournament = cruds.tournament.get(db=db, id=id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    tournament = cruds.tournament.update(db=db, db_obj=tournament, obj_in=tournament_in)
    return tournament


@router.delete("/{id}", response_model=schemas.Tournament)
async def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a tournament.
    """
    tournament = cruds.tournament.get(db=db, id=id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    tournament = cruds.tournament.remove(db=db, id=id)
    return tournament

