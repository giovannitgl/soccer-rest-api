from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import cruds, schemas
from server.api import deps
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


@router.get("/{tournament_id}/match", response_model=List[schemas.Match])
async def list_matches(
    tournament_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT,
) -> Any:
    """
    List matches in a tournament
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return cruds.match.get_multi(db, skip=skip, limit=limit)


@router.get("/{tournament_id}/match", response_model=schemas.Match)
async def list_match(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    match_id: int

) -> Any:
    """
    List matchs.
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    match = cruds.match.get(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.post("/{tournament_id}/match", response_model=schemas.Match)
async def create_match(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    match_in: schemas.MatchCreate
) -> Any:
    """
    Create new match.
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    match = cruds.match.create(db=db, obj_in=match_in)
    return match


@router.put("/{tournament_id}/match/{match_id}", response_model=schemas.Match)
async def update_match(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    match_id: int,
    match_in: schemas.MatchUpdate
) -> Any:
    """
    Update a match.
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    match = cruds.match.get(db=db, id=match_id, tournament_id=tournament_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match = cruds.match.update(db=db, db_obj=match, obj_in=match_in)
    return match


@router.delete("/{tournament_id}/match/{match_id}", response_model=schemas.Match)
async def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    match_id: int
) -> Any:
    """
    Delete a match.
    """
    match = cruds.match.get(db=db, id=match_id, tournament_id=tournament_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match = cruds.match.remove(db=db, id=match_id)
    return match
