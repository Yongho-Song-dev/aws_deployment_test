from sqlalchemy import create_engine, MetaData,  engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.collections import InstrumentedList as _InstrumentedList

from contextlib import contextmanager
from typing import Iterator, Optional, TypeVar
from functools import lru_cache

# from .boto_key import *
from .settings import get_database_settings

import json
import base64
import os, logging



# Should save this info into AWS Secrets Manager
# secret_manager = aws('database')
# secret = secret_manager.get_secret()

def load_json():
    with open("./api/database/secret.json", 'r') as f :
        json_data = json.load(f)
        
    return json_data
        
secret = load_json()
# print(json.dumps(json_data))




SQLALCHEMY_DATABASE_URL = '{}://{}:{}@{}:{}/{}'.format(
    # secret['database']['type'],
    # secret['database']['user'],
    # secret['database']['password'],
    # secret['database']['host'],
    # secret['database']['port'],
    # secret['database']['database']
    secret['type'],
    secret['user'],
    secret['password'],
    secret['host'],
    secret['port'],
    secret['database']
)

sql_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
    pool_recycle=500, 
    pool_size=5,
    encoding='utf-8'
)

SessionLocal = sessionmaker(bind=sql_engine, autocommit=False, autoflush=False)

Base = declarative_base()


# @lru_cache
def get_engine() -> engine.Engine:
    db_settings = get_database_settings()
    uri = db_settings.sqlalchemy_uri
    log_sqlalchemy_sql_statements = db_settings.log_sqlalchemy_sql_statements
    return get_new_engine(uri, log_sqlalchemy_sql_statements)

# @lru_cache
def get_new_engine(uri: str, log_sqlalchemy_sql_statements: bool = False,) -> engine.Engine:
    if log_sqlalchemy_sql_statements:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    else:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    kwargs = {
        'pool_pre_ping':True, 
        'pool_recycle':500, 
        'pool_size':6,
        'encoding':'utf-8'
    }
    return create_engine(uri, **kwargs)


def get_sessionmaker() -> sessionmaker:
    return get_sessionmaker_for_engine(get_engine()) # sessionmaker를 return 

def get_session() -> engine.Engine:
    """
        engine이 있는 경우 그대로 session을 사용
    """
    return get_sessionmaker()()

def get_sessionmaker_for_engine(engine: engine.Engine) -> engine.Engine:
    """
        engine이 없는 경우 sessionmaker을 활용해서 새롭게 bind 시켜준다.
    """
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() ->Iterator[Session]:
    """
        FastAPI 종속성을 위해 사용 ( Depends )
    """
    yield from _get_db()


def _get_db(engine: Optional[engine.Engine] = None) -> Iterator[Session]:
    if engine is None:
        session = get_session()
    else: 
        session = get_sessionmaker_for_engine(engine)()
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()



@contextmanager
def context_session(engine: Optional[engine.Engine] = None) -> Iterator[Session]:
    yield from _get_db(engine)
