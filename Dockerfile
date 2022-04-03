FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update -y; apt-get upgrade -y; apt-get install -y libpq-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./wait-for-it.sh /code
COPY ./alembic.ini /code
COPY ./alembic /code/alembic
COPY ./server /code/server
COPY ./start.sh /code/

RUN chmod +x /code/start.sh; chmod +x /code/wait-for-it.sh
CMD ["sh", "./start.sh"]