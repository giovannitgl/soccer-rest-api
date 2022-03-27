from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from server import cruds, schemas
from server.api import deps
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


@router.get("/", response_model=List[schemas.Team])
def list_teams(
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
    return cruds.team.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=schemas.Team)
def list_team(
        *,
        db: Session = Depends(deps.get_db),
        id: int
) -> Any:
    """
    List teams.
    """
    team = cruds.team.get(db, id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/", response_model=schemas.Team)
def create_team(
    *,
    db: Session = Depends(deps.get_db),
    team_in: schemas.TeamCreate
) -> Any:
    """
    Create new team.
    """
    team = cruds.team.create(db=db, obj_in=team_in)
    return team


@router.put("/{id}", response_model=schemas.Team)
def update_team(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    team_in: schemas.TeamUpdate
) -> Any:
    """
    Update a team.
    """
    team = cruds.team.get(db=db, id=id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team = cruds.team.update(db=db, db_obj=team, obj_in=team_in)
    return team


@router.delete("/{id}", response_model=schemas.Team)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a team.
    """
    team = cruds.team.get(db=db, id=id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team = cruds.team.remove(db=db, id=id)
    return team
