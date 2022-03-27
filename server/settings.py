from os import environ

DATABASE_URL = environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/db')
