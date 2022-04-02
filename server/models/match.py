from sqlalchemy import Column, Integer, ForeignKey, DateTime

from server.database import Base


class Match(Base):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournament.id"), nullable=False)
    team_1_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    team_2_id = Column(Integer, ForeignKey("team.id"), nullable=False)
