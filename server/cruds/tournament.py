from sqlalchemy.orm import Session

from server.cruds.base import CRUDBase
from server.models import Tournament, Team
from server.schemas import TournamentCreate, TournamentUpdate


class CRUDTournament(CRUDBase[Tournament, TournamentCreate, TournamentUpdate]):
    def add_team(
            self,
            db: Session,
            *,
            tournament: Tournament,
            team: Team,
    ) -> Tournament:
        teams = tournament.teams
        teams.append(team)
        teams = list(set(teams))
        tournament.teams = teams
        db.add(tournament)
        db.commit()
        db.refresh(tournament)
        return tournament

    def remove_team(
            self,
            db: Session,
            *,
            tournament: Tournament,
            team: Team,
    ) -> Tournament:
        teams = tournament.teams
        teams.remove(team)
        tournament.teams = teams
        db.add(tournament)
        db.commit()
        db.refresh(tournament)
        return tournament


tournament = CRUDTournament(Tournament)
