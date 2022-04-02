from server.cruds.base import CRUDBase
from server.models import MatchEvent
from server.schemas import MatchEventCreate, MatchEventUpdate


class CRUDMatchEvent(CRUDBase[MatchEvent, MatchEventCreate, MatchEventUpdate]):
    pass


match_event = CRUDMatchEvent(MatchEvent)
