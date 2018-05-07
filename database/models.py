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
    tv_show_link = Column(String)
    episode_link = Column(String)

    def __init__(self, title_ru, title_en, jpg, date, season, tv_show_link, episode_link):
        self.title_en = title_en
        self.title_ru = title_ru
        self.jpg = jpg
        self.date = date
        self.season = season
        self.tv_show_link = tv_show_link
        self.episode_link = episode_link

    def __repr__(self):
        return '{"title_ru": "%s", "title_en": "%s", "jpg": "%s", "date": "%s", "season": "%s", \
               "tv_show_link": "%s", "episode_link": "%s"}' % (
                    self.title_ru,
                    self.title_en,
                    self.jpg,
                    self.date,
                    self.season,
                    self.tv_show_link,
                    self.episode_link
                )


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    when_check = Column(DateTime, nullable=True)
    notify_sound = Column(Boolean)
    time_notify_start = Column(Time, nullable=True)
    time_notify_stop = Column(Time, nullable=True)
    spy = Column(Boolean)
    timezone = Column(String, nullable=True)
    notify_timer = Column(Boolean)

    def __init__(self, chat_id, notify_sound, spy, notify_timer):
        self.chat_id = chat_id
        self.notify_sound = notify_sound
        self.spy = spy
        self.notify_timer = notify_timer

    def __repr__(self):
        return '{"chat_id": "%s", "when_check": %s, "notify_sound": "%s", "time_notify_start": "%s", ' \
               '"time_notify_stop": "%s", "spy": "%s", "timezone": "%s", "notify_timer": "%s"}' % (
                    self.chat_id,
                    self.when_check,
                    self.notify_sound,
                    self.time_notify_start,
                    self.time_notify_stop,
                    self.spy,
                    self.timezone,
                    self.notify_timer
                )
