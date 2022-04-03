import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Session
from sqlalchemy_utils import ChoiceType

from server.database import Base
from server.models import Player


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

    def get_event_message(self, db: Session) -> str:
        # Get player names on db
        player1_name = ''
        if self.player_id:
            player = db.query(Player).filter(Player.id == id).first()
            if player:
                player1_name = f'{player.first_name} {player.last_name}'

        player2_name = ''
        if self.integer_value and self.event_type == EventType.substitution:
            player = db.query(Player).filter(Player.id == id).first()
            if player:
                player2_name = f'{player.first_name} {player.last_name}'

        messages = {
            EventType.start: f'Match started at {self.time}',
            EventType.goal: f'Goal from player {player1_name} at {self.time}',
            EventType.half_time: f'Half time at {self.time}',
            EventType.stoppage_time: f'Stoppage time at {self.time}. Duration {self.integer_value} minutes',
            EventType.substitution: f'Substitution at {self.time}. {player1_name} out,'
                                    f' {player2_name} in',
            EventType.warning: f'{player1_name} received a {self.string_value}',
            EventType.end: f'Match finished at {self.time}'
        }
        return messages[self.event_type]


