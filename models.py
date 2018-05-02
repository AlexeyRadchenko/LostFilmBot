from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TVShow(Base):
    __tablename__ = 'tv_shows'
    id = Column(Integer, primary_key=True)
    title_ru = Column(String(collation='utf8'))
    title_en = Column(String(collation='utf8'))
    description = Column(String(collation='utf8'))
    jpg = Column(String(collation='utf8'))


class LastTVShow(Base):
     __tablename__ = 'last_tv_shows'
     id = Column(Integer, primary_key=True)
     title_ru = Column(String(collation='utf8'))
     title_en = Column(String(collation='utf8'))
     jpg = Column(String(collation='utf8'))
     date = Column(Date)
     season = Column(String(collation='utf8'))
     #perso = Column(Integer, ForeignKey(Person.id))


class UserWhoCheckAntispam(Base):
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInt)
    when_check = (Data)

class UserHasId(Base):
    user_id = Column()
    serial_id = Column()