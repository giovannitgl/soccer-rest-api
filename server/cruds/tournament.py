from server.cruds.base import CRUDBase
from server.models import Tournament
from server.schemas import TournamentCreate, TournamentUpdate


class CRUDTournament(CRUDBase[Tournament, TournamentCreate, TournamentUpdate]):
    pass


tournament = CRUDTournament(Tournament)
