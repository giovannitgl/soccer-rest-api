from typing import List

from sqlalchemy.orm import Session

from server.cruds.base import CRUDBase
from server.models import Team
from server.schemas import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def get_multi_by_ids(
            self, db: Session, *, ids: List[int], skip: int = 0, limit: int = 100
    ) -> List[Team]:
        return db.query(self.model).filter(Team.id.in_(ids)).offset(skip).limit(limit).all()


team = CRUDTeam(Team)
