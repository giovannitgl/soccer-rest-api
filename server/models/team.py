from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from server.database import Base


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    players = relationship("Player")
