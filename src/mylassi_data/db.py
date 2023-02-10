__all__ = ['engine', 'Base', 'SessionLocal', 'get_db']

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv('.env')
SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']
SQLALCHEMY_DB_POOL_SIZE = os.environ.get('DB_POOL_SIZE', 20)
SQLALCHEMY_DB_MAX_OVERFLOW = os.environ.get('DB_MAX_OVERFLOW', 20)

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=SQLALCHEMY_DB_POOL_SIZE, max_overflow=SQLALCHEMY_DB_MAX_OVERFLOW)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata)


def get_db():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()
