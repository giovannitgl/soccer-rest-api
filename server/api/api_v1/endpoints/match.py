from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import cruds, schemas
from server.api import deps
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


@router.get("/", response_model=List[schemas.Match])
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
    return cruds.match.get_multi_with_tournament(db, tournament_id=tournament_id, skip=skip, limit=limit)


@router.get("/{match_id}", response_model=schemas.Match)
async def list_match(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    match_id: int
) -> Any:
    """
    Detail a match.
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    match = cruds.match.get_with_tournament(db, match_id, tournament_id=tournament_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.post("/", response_model=schemas.Match)
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
    if not tournament.team_in_tournament(match_in.team_1_id) or not tournament.team_in_tournament(match_in.team_2_id):
        raise HTTPException(status_code=422, detail="Teams must be in the tournament")
    match_create = schemas.MatchCreateInternal(**match_in.__dict__, tournament_id=tournament_id)
    match = cruds.match.create(db=db, obj_in=match_create)
    return match


@router.put("/{match_id}", response_model=schemas.Match)
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
    match = cruds.match.get_with_tournament(db=db, id=match_id, tournament_id=tournament_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match = cruds.match.update(db=db, db_obj=match, obj_in=match_in)
    return match


@router.delete("/{match_id}", response_model=schemas.Match)
async def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    match_id: int
) -> Any:
    """
    Delete a match.
    """
    match = cruds.match.get_with_tournament(db=db, id=match_id, tournament_id=tournament_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match = cruds.match.remove(db=db, id=match_id)
    return match
