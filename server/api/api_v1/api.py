from fastapi import APIRouter

from server.api.api_v1.endpoints import player, team, transfer, tournament, tournament_team, match, match_event

api_router = APIRouter()
api_router.include_router(player.router, prefix='/player', tags=['player'])
api_router.include_router(team.router, prefix='/team', tags=['team'])
api_router.include_router(transfer.router, prefix='/transfer', tags=['transfer'])
api_router.include_router(tournament.router, prefix='/tournament', tags=['tournament'])

# Sub Routes
api_router.include_router(tournament_team.router, prefix='/tournament/{tournament_id}/team', tags=['tournament teams'])
api_router.include_router(match.router, prefix='/tournament/{tournament_id}/match', tags=['tournament matches'])
api_router.include_router(match_event.router, prefix='/tournament/{tournament_id}/match/{match_id}/event',
                          tags=['tournament events'])

