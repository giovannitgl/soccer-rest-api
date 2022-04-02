from fastapi import APIRouter

from server.api.api_v1.endpoints import player, team, transfer, tournament

api_router = APIRouter()
api_router.include_router(player.router, prefix='/player', tags=['player'])
api_router.include_router(team.router, prefix='/team', tags=['team'])
api_router.include_router(transfer.router, prefix='/transfer', tags=['transfer'])
api_router.include_router(tournament.router, prefix='/tournament', tags=['tournament'])

