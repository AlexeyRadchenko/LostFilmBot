from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, BigInteger, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TVShow(Base):
    __tablename__ = 'tv_shows'
    id = Column(Integer, primary_key=True)
    title_ru = Column(String)
    title_en = Column(String)
    description = Column(String)
    jpg = Column(String)

    def __init__(self, title_ru, title_en, description, jpg):
        self.title_en = title_en
        self.title_ru = title_ru
        self.description = description
        self.jpg = jpg

    def __repr__(self):
        return "<TVShow('%s','%s', '%s', '%s')>" % (self.title_ru, self.title_en, self.jpg, self.description)


class LastTVShow(Base):
    __tablename__ = 'last_tv_shows'
    id = Column(Integer, primary_key=True)
    title_ru = Column(String)
    title_en = Column(String)
    jpg = Column(String)
    date = Column(Date)
    season = Column(String)


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    when_check = Column(DateTime)
    notify_sound = Column(Boolean)
    time_notify_start = Column(Time)
    time_notify_stop = Column(Time)
    spy = Column(Boolean)

