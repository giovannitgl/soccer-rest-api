from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from server.database import Base


class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    country = Column(String, nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'))
