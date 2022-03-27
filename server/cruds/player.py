from server.cruds.base import CRUDBase
from server.models import Player
from server.schemas import PlayerCreate, PlayerUpdate


class CRUDPlayer(CRUDBase[Player, PlayerCreate, PlayerUpdate]):
    pass


player = CRUDPlayer(Player)
