from os import environ

PROJECT_NAME: str = environ.get('PROJECT_NAME', 'Soccer API')
DATABASE_URL: str = environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/db')

API_V1_STR: str = '/api/v1'

DEFAULT_PAGE: int = 0
DEFAULT_LIMIT: int = 10

SEND_EVENTS_TO_QUEUE = environ.get('SEND_EVENTS_TO_QUEUE', 'true') == 'true'
RABBITMQ_HOST = environ.get('RABBITMQ_HOST', 'localhost')
