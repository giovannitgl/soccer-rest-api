from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import cruds, schemas
from server.api import deps
from server.api.api_v1.endpoints import match
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


@router.get("/", response_model=List[schemas.Team])
async def list_tournament_teams(
    tournament_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT
) -> Any:
    """
    List tournament teams
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    ids = [team.id for team in tournament.teams]
    return cruds.team.get_multi_by_ids(db, ids=ids, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Tournament)
async def add_tournament_team(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    tournament_in: schemas.TournamentAddTeam
) -> Any:
    """
    Add team to a tournament
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    team = cruds.team.get(db=db, id=tournament_in.team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    tournament = cruds.tournament.add_team(db=db, tournament=tournament, team=team)
    return tournament


@router.delete("/{team_id}", response_model=schemas.Tournament)
async def remove_team_from_tournament(
    *,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    team_id: int,
) -> Any:
    """
    Delete a tournament.
    """
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    team = cruds.team.get(db=db, id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    tournament = cruds.tournament.remove_team(db=db, tournament=tournament, team=team)
    return tournament
