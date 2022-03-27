from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric

from server.database import Base


class Transfer(Base):
    __tablename__ = 'transfer'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    player_id = Column(Integer, ForeignKey('player.id'))
    origin_team_id = Column(Integer, ForeignKey('team.id'))
    destination_team_id = Column(Integer, ForeignKey('team.id'))
