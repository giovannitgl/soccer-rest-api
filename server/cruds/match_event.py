from typing import List

from sqlalchemy.orm import Session

from server.cruds.base import CRUDBase
from server.models import MatchEvent, Tournament
from server.schemas import MatchEventCreate, MatchEventUpdate


class CRUDMatchEvent(CRUDBase[MatchEvent, MatchEventCreate, MatchEventUpdate]):
    def get_multi_for_match(
            self, db: Session, *, match_id: int, skip: int = 0, limit: int = 100
    ) -> List[MatchEvent]:
        return db.query(self.model)\
            .filter(self.model.match_id == match_id)\
            .offset(skip).limit(limit).all()


match_event = CRUDMatchEvent(MatchEvent)
