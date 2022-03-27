from server.cruds.base import CRUDBase
from server.models import Team
from server.schemas import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    pass


team = CRUDTeam(Team)
