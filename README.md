# Soccer API
This is a project done for an assignment, containing a RESTful API with models related to soccer.
It is not in a complete state for running in a production environment, but feel free to modify and test it.

The project was done using FastAPI

## Documentation
When running the api you can access the swagger interface:
``/docs``

You can also download the openAPI specification on 
```
GET /api/v1/openapi.json
```

## How to run
This project was developed using postgres as the database provider, you can set the URL settings the DATABASE_URL env var.

Optionally, this project contains a pub/sub based on rabbitmq. If you with to run it cofigure the following enviroment variables:
```bash
SEND_EVENTS_TO_QUEUE=true
RABBITMQ_HOST=#whatever the host for you instance is
```

### Running on terminal
You can run directly from your terminal the start.sh file, which will execute the following commands:
```bash
alembic upgrade head
uvicorn app.main:server --host "0.0.0.0" --port 8000
```


### Docker compose
Optionally, you can run this project using the Makefile commands, which will use docker-compose.
Again this is not a production ready environment.

```
make build
make run
```

## Pub/Sub
To test the pub/sub feature, you can run extra/consumer.py to check the messages being received.
If you have a match with id 1 and 2, for example, you can run the following command:
```bash
python extra/consumer.py match:1 match:2
```
You will receive all the events created for them in a serialized json format.
