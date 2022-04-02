from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from server.database import Base

# Auxiliary table used for many to many relationship between tournament and teams
tournament_teams = Table('tournament_teams', Base.metadata,
                         Column('tournament_id', ForeignKey('tournament.id')),
                         Column('team_id', ForeignKey('team.id')),
                         )


class Tournament(Base):
    __tablename__ = 'tournament'
    id = Column(Integer, primary_key=True, index=True)
    start_day = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    teams = relationship("Team", secondary=tournament_teams)

    def team_in_tournament(self, team_id):
        ids = [team.id for team in self.teams]
        return team_id in ids
