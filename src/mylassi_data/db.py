__all__ = ['engine', 'Base', 'SessionLocal', 'get_db']

import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///./sql_app.db")

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

is_postgres = SQLALCHEMY_DATABASE_URL.startswith('postgresql+psycopg2://')

create_engine_args = dict()

if is_postgres:
    create_engine_args['pool_size'] = os.environ.get('DB_POOL_SIZE', 20)
    create_engine_args['max_overflow'] = os.environ.get('DB_MAX_OVERFLOW', 20)

engine = create_engine(SQLALCHEMY_DATABASE_URL, **create_engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata)


def get_db():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
