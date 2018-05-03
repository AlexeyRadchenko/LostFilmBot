from parser.parser import LostFilmParser
from database.database_init import engine_selector
from database.models import LastTVShow
import dateparser

engine, Session = engine_selector()
session = Session()
#session.add(myobject)
#session.commit()


def start(bot, update):
    print(update.message)
    username = update.message.chat.first_name
    text = f'Привет, {username}.' \
           f' Я бот, который сообщает о новых сериалах и новых сериях на Lostfilm.tv\n' \
           f'Вот список моих команд :\n' \
           f'Check - проверить последние новинки\n' \
           f'Spy - начать слежку за новинками ;)\n' \
           f'Stop - прекратить слежку'
    bot.send_message(chat_id=update.message.chat_id, text=text)


def help(bot, update):
    text = 'Вот список моих команд :\n' \
           'Check - проверить последние новинки\n' \
           'Spy - начать слежку за новинками ;)\n' \
           'Stop - прекратить слежку'
    bot.send_message(chat_id=update.message.chat_id, text=text)


def check(bot, update):
    episodes_in_request = LostFilmParser().get_new_shows_episodes()
    episodes_in_db = session.query(LastTVShow).all()
    if not episodes_in_db:
        for episode in episodes_in_request:
            caption = '{0} - {1}\nО сериале: {2}'.format(
                episode['title_ru'], episode['season'], episode['tv_show_link'])
            bot.sendPhoto(chat_id=update.message.chat_id, photo=episode['jpg'], caption=caption)
            db_object = LastTVShow(
                episode['title_ru'],
                episode['title_en'],
                episode['jpg'],
                dateparser.parse(episode['date']),
                episode['season'],
                episode['tv_show_link'],
                episode['episode_link'],
            )
            session.add(db_object)
        session.commit()
    else:
        print('second')
        bot.send_message(chat_id=update.message.chat_id, text='Это последние новинки')


def spy(bot, update):
    pass
"""
new_episodes = LostFilmParser().get_new_shows_episodes()
episodes_in_db = session.query(LastTVShow).all()
print(episodes_in_db)"""