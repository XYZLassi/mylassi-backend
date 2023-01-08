__all__ = ['engine', 'session', 'Base']

import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from dotenv import load_dotenv

load_dotenv('.env')

SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base(metadata=metadata)
Base.query = session.query_property()
