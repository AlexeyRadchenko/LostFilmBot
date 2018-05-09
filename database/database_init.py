from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os.path import abspath
import conf
from database import models


def engine_selector():
    if conf.DEBUG:
        sqlite_path = 'sqlite:///{0}/LFbot.db'.format(abspath('./'))
        engine = create_engine(sqlite_path, echo=False)
    else:
        engine = create_engine(conf.DB_CONNECT, echo=False)

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return engine, db_session


def init_db():
    engine, db_session = engine_selector()
    models.Base.metadata.create_all(engine)
    models.Base.query = db_session.query_property()
""" Здесь нужно импортировать все модули, где могут быть определены модели,
    которые необходимым образом могут зарегистрироваться в метаданных.
    В противном случае их нужно будет импортировать до вызова init_db()"""
