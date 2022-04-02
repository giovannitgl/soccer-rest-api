from typing import Optional, List

from sqlalchemy.orm import Session

from server.cruds.base import CRUDBase
from server.models import Match
from server.schemas import MatchCreate, MatchUpdate


class CRUDMatch(CRUDBase[Match, MatchCreate, MatchUpdate]):
    def get_multi_with_tournament(
            self, db: Session, *, tournament_id: int, skip: int = 0, limit: int = 100
    ) -> List[Match]:
        return db.query(self.model).filter(self.model.tournament_id == tournament_id).offset(skip).limit(limit).all()

    def get_with_tournament(self, db: Session, id: int, tournament_id: int) -> Optional[Match]:
        return db.query(self.model).filter(self.model.id == id, self.model.tournament_id == tournament_id).first()


match = CRUDMatch(Match)
