from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os.path import abspath
import models


def engine_selector(conf_type, path):
    if conf_type == 'dev':
        if not path:
            sqllite_path ='sqlite:///{0}/LFbot.db'.format(abspath('./'))
            engine = create_engine(sqllite_path, echo=False)
    elif conf_type == 'prod':
        pass

    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return engine, db_session


def init_db(conf_type='dev', path=None):
    engine, db_session = engine_selector(conf_type, path)
    models.Base.metadata.create_all(engine)
    models.Base.query = db_session.query_property()
    # Здесь нужно импортировать все модули, где могут быть определены модели,
    # которые необходимым образом могут зарегистрироваться в метаданных.
    # В противном случае их нужно будет импортировать до вызова init_db()

init_db()
