import logging

from fastapi import FastAPI

from server import settings
from server.api.api_v1.api import api_router
from server.queue.rabbitmq import RabbitClient

from prometheus_fastapi_instrumentator import Instrumentator

logger = logging.getLogger(__name__)


class SoccerAPI(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings.SEND_EVENTS_TO_QUEUE:
            self.rabbit_client = RabbitClient()


app = SoccerAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event('shutdown')
def shutdown_queue():
    if settings.SEND_EVENTS_TO_QUEUE:
        app.rabbit_client.connection.close()


Instrumentator().instrument(app).expose(app, include_in_schema=False)

