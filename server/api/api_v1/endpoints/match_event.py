from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from server import cruds, schemas, settings, models
from server.api import deps
from server.queue.rabbitmq import RabbitClient
from server.settings import DEFAULT_PAGE, DEFAULT_LIMIT

router = APIRouter()


def validate_exists(db: Session, tournament_id: int, match_id: int) -> None:
    tournament = cruds.tournament.get(db=db, id=tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    match = cruds.match.get(db=db, id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.tournament_id != tournament.id:
        raise HTTPException(status_code=400, detail="Match does not belong to this tournament")


def send_to_queue(client: RabbitClient, match_id: int, event: schemas.MatchEventOutput) -> None:
    if settings.SEND_EVENTS_TO_QUEUE:
        routing_key = f'match:{match_id}'
        message = event.json()
        client.publish_to_topic(routing_key, message)


@router.get("/", response_model=List[schemas.MatchEventOutput])
async def list_events(
    tournament_id: int,
    match_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = DEFAULT_PAGE,
    limit: int = DEFAULT_LIMIT,
) -> Any:
    """
    List events in a match
    """
    validate_exists(db, tournament_id, match_id)
    events = cruds.match_event.get_multi_for_match(db, match_id=match_id, skip=skip, limit=limit)
    messages = []
    for event in events:
        messages.append(schemas.MatchEventOutput(
            time=event.time,
            message=event.event.get_event_message(db, event)
        ))
    return messages


@router.post("/start", response_model=schemas.MatchEventOutput)
async def register_start(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    tournament_id: int,
    match_id: int,
    event_in: schemas.MatchEventStartCreate
) -> Any:
    """
    Register the start of the match
    """
    validate_exists(db, tournament_id, match_id)
    event_create = schemas.MatchEventCreateInternal(**event_in.__dict__,
                                                    match_id=match_id, event_type=models.EventType.start)
    event = cruds.match_event.create(db=db, obj_in=event_create)
    event = schemas.MatchEventOutput(time=event.time, message=event.get_event_message(db, event))
    send_to_queue(request.app.rabbit_client, match_id, event)
    return event


@router.post("/end", response_model=schemas.MatchEventOutput)
async def register_end(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        tournament_id: int,
        match_id: int,
        event_in: schemas.MatchEventEndCreate
) -> Any:
    """
    Register the end of the game
    """
    validate_exists(db, tournament_id, match_id)
    event_create = schemas.MatchEventCreateInternal(**event_in.__dict__,
                                                    match_id=match_id, event_type=models.EventType.end)
    event = cruds.match_event.create(db=db, obj_in=event_create)
    event = schemas.MatchEventOutput(time=event.time, message=event.get_event_message(db, event))
    send_to_queue(request.app.rabbit_client, match_id, event)
    return event


@router.post("/goal", response_model=schemas.MatchEventOutput)
async def register_goal(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        tournament_id: int,
        match_id: int,
        event_in: schemas.MatchEventGoalCreate
) -> Any:
    """
    Register a goal for a team
    """
    validate_exists(db, tournament_id, match_id)
    data = event_in.__dict__
    data['integer_field'] = data['team_id']
    del data['team_id']
    event_create = schemas.MatchEventCreateInternal(**data,  match_id=match_id,
                                                    event_type=models.EventType.goal)
    event = cruds.match_event.create(db=db, obj_in=event_create)
    event = schemas.MatchEventOutput(time=event.time, message=event.get_event_message(db, event))
    send_to_queue(request.app.rabbit_client, match_id, event)
    return event


@router.post("/halftime", response_model=schemas.MatchEventOutput)
async def register_half_time(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        tournament_id: int,
        match_id: int,
        event_in: schemas.MatchEventHalfTimeCreate
) -> Any:
    """
    Registers half time for the match
    """
    validate_exists(db, tournament_id, match_id)
    event_create = schemas.MatchEventCreateInternal(**event_in.__dict__,
                                                    match_id=match_id, event_type=models.EventType.half_time)
    event = cruds.match_event.create(db=db, obj_in=event_create)
    event = schemas.MatchEventOutput(time=event.time, message=event.get_event_message(db, event))
    send_to_queue(request.app.rabbit_client, match_id, event)
    return event


@router.post("/stoppage", response_model=schemas.MatchEventOutput)
async def register_stoppage(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        tournament_id: int,
        match_id: int,
        event_in: schemas.MatchEventStoppageCreate
) -> Any:
    """
    Registers stoppage in the match
    """
    validate_exists(db, tournament_id, match_id)
    data = event_in.__dict__
    data['integer_field'] = data['minutes']
    del data['minutes']
    event_create = schemas.MatchEventCreateInternal(**data,  match_id=match_id,
                                                    event_type=models.EventType.stoppage_time)
    event = cruds.match_event.create(db=db, obj_in=event_create)
    event = schemas.MatchEventOutput(time=event.time, message=event.get_event_message(db, event))
    send_to_queue(request.app.rabbit_client, match_id, event)
    return event


@router.post("/substitution", response_model=schemas.MatchEventOutput)
async def register_substitution(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        tournament_id: int,
        match_id: int,
        event_in: schemas.MatchEventSubstitutionCreate
) -> Any:
    """
    Registers a player substitution in a match
    """
    validate_exists(db, tournament_id, match_id)
    data = event_in.__dict__
    data['player_id'] = data['player_out']
    data['integer_field'] = data['player_in']
    del data['player_in']
    del data['player_out']
    event_create = schemas.MatchEventCreateInternal(**data,  match_id=match_id,
                                                    event_type=models.EventType.substitution)
    event = cruds.match_event.create(db=db, obj_in=event_create)
    event = schemas.MatchEventOutput(time=event.time, message=event.get_event_message(db, event))
    send_to_queue(request.app.rabbit_client, match_id, event)
    return event


@router.post("/warning", response_model=schemas.MatchEventOutput)
async def register_warning(
        *,
        request: Request,
        db: Session = Depends(deps.get_db),
        tournament_id: int,
        match_id: int,
        event_in: schemas.MatchEventWarningCreate
) -> Any:
    """
    Registers a player substitution in a match
    """
    validate_exists(db, tournament_id, match_id)
    data = event_in.__dict__
    data['string_field'] = data['warning_type']
    del data['warning_type']
    event_create = schemas.MatchEventCreateInternal(**data,  match_id=match_id,
                                                    event_type=models.EventType.warning)
    event = cruds.match_event.create(db=db, obj_in=event_create)
    event = schemas.MatchEventOutput(time=event.time, message=event.get_event_message(db, event))
    send_to_queue(request.app.rabbit_client, match_id, event)
    return event
