from server.cruds.base import CRUDBase
from server.models import Match
from server.schemas import MatchCreate, MatchUpdate


class CRUDMatch(CRUDBase[Match, MatchCreate, MatchUpdate]):
    pass


match = CRUDMatch(Match)
