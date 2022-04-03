import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Session
from sqlalchemy_utils import ChoiceType

from server import cruds
from server.database import Base


class EventType(int, enum.Enum):
    start = 1
    goal = 2
    half_time = 3
    stoppage_time = 4
    substitution = 5
    warning = 6
    end = 7


class MatchEvent(Base):
    __tablename__ = 'match_event'
    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("match.id"), nullable=False)
    time = Column(DateTime, nullable=False)
    event_type = Column(ChoiceType(EventType, impl=Integer()))
    player_id = Column(Integer, ForeignKey("player.id"), nullable=True)
    string_value = Column(String, nullable=True)
    integer_value = Column(Integer, nullable=True)


def get_event_message(db: Session, match_event: MatchEvent) -> str:
    # Get player names on db
    player1_name = ''
    if match_event.player_id:
        player = cruds.player.get(db, match_event.player_id)
        if player:
            player1_name = f'{player.first_name} {player.last_name}'

    player2_name = ''
    if match_event.integer_value and match_event.event_type == EventType.substitution:
        player = cruds.player.get(db, match_event.player_id)
        if player:
            player2_name = f'{player.first_name} {player.last_name}'

    messages = {
        EventType.start: f'Match started at {match_event.time}',
        EventType.goal: f'Goal from player {player1_name} at {match_event.time}',
        EventType.half_time: f'Half time at {match_event.time}',
        EventType.stoppage_time: f'Stoppage time at {match_event.time}. Duration {match_event.integer_value} minutes',
        EventType.substitution: f'Substitution at {match_event.time}. {player1_name} out,'
                                f' {player2_name} in',
        EventType.warning: f'{player1_name} received a {match_event.string_value}',
        EventType.end: f'Match finished at {match_event.time}'
    }
    return messages[match_event.event_type]
