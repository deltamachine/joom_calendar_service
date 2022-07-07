import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from core.settings import settings


# настройка подключения к PostgreSQL
DB_USER = settings.db_user
DB_PASS = settings.db_password
DB_HOST = settings.db_host
DB_NAME = settings.db_name
DB_PORT = settings.db_port

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

TESTING_SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/test_{settings.db_name}'

if not database_exists(TESTING_SQLALCHEMY_DATABASE_URL):
    create_database(TESTING_SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
testing_engine = create_engine(TESTING_SQLALCHEMY_DATABASE_URL)

if "pytest" in sys.argv[0]:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)
else:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
