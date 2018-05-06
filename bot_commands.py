from parser.parser import LostFilmParser
from database.database_init import engine_selector
from database.models import LastTVShow, UserProfile
import dateparser, json, conf
from utils import get_new_episode, build_menu, flag
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from emoji import emojize
from datetime import datetime
engine, Session = engine_selector()
session = Session()


def start(bot, update):
    username = update.message.chat.first_name
    user_db = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    if not user_db:
        db_object = UserProfile(
            chat_id=update.message.chat_id,
            notify_sound=True,
            spy=False
        )
        session.add(db_object)
        session.commit()
        status = emojize(':no_entry_sign:', use_aliases=True)
    else:
        if user_db.spy:
            status = emojize(":white_check_mark:", use_aliases=True)
        else:
            status = emojize(':no_entry_sign:', use_aliases=True)
    button_list = [
        [KeyboardButton('Новинки'), KeyboardButton('Уведомления ' + status)],
        [KeyboardButton('Настройка уведомлений')],
        [KeyboardButton('Звук уведомлений(on)')]
    ]
    #reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True)
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=conf.START_TEXT.format(username), reply_markup=reply_markup)


def help(bot, update):
    print(update.message)
    bot.send_message(chat_id=update.message.chat_id, text=conf.HELP_TEXT)


def settings(bot, update):
    """button_list = [
        KeyboardButton(""),
        KeyboardButton("Следить"),
        KeyboardButton("Стоп"),
        KeyboardButton('Настройка уведомлений')
    ]"""
    button_list = [KeyboardButton(timezone) for timezone in conf.PY_TIMEZONES_RU['timezones']]
    button_list.append(KeyboardButton('Меню'))
    #reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=3), resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Выберите часовой пояс", reply_markup=reply_markup)


def timezone_set(bot, update):
    reply_markup = ReplyKeyboardRemove()
    print(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text="Укажите время когда сообщения должны быть без звука в 24-х часовом формате, пример 23-8 (с 23 ночи до 8 часов сообения будут беззвучными)", reply_markup=reply_markup)


def silent_time(bot, update):
    print(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text="Время установленно")


def check(bot, update):
    episodes_in_request = LostFilmParser().get_new_shows_episodes()
    episodes_in_db = session.query(LastTVShow).all()
    user_db = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    if not user_db.__dict__['when_check']:
        session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).update(
            {
                'when_check': datetime.now()
            }
        )
    else:
        if user_db.__dict__['timezone']:
            pass

    """    
    session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).update(
        {
            'when_check': datetime.now()
        }
    )
    """
    if not episodes_in_db:
        for episode in episodes_in_request:
            caption = conf.EPISODE_CAPTION.format(
                episode['title_ru'], episode['season'], episode['tv_show_link'])
            bot.sendPhoto(chat_id=update.message.chat_id,
                          photo=episode['jpg'], caption=caption
                          )
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
        for episode in episodes_in_request:
            caption = conf.EPISODE_CAPTION.format(
                episode['title_ru'], episode['season'], episode['tv_show_link'])
            bot.sendPhoto(chat_id=update.message.chat_id, photo=episode['jpg'], caption=caption)
    bot.send_message(chat_id=update.message.chat_id, text=conf.AFTER_CHECK_TEXT)


def spy(bot, update):
    print(update.message.date)
    #print(dateparser.parse(update.message.date))
    bot.send_message(chat_id=update.message.chat_id, text='date')


def updater_task(bot, job):
    new_episodes = LostFilmParser().get_new_shows_episodes()
    episodes_in_db = session.query(LastTVShow).all()
    set_episodes_in_db = set([episode.__dict__['title_ru'] for episode in episodes_in_db])
    set_all_new_episodes = set([episode['title_ru'] for episode in new_episodes])
    diff_set_old_episodes = set_episodes_in_db - set_all_new_episodes
    diff_set_new_episodes = set_all_new_episodes - set_episodes_in_db
    if diff_set_old_episodes:
        for old_episode in diff_set_old_episodes:
            for new_episode_title in diff_set_new_episodes:
                new_episode = get_new_episode(new_episode_title, new_episodes)
                caption = conf.EPISODE_CAPTION.format(
                    new_episode['title_ru'], new_episode['season'], new_episode['tv_show_link'])
                bot.sendPhoto(chat_id=219915673, photo=new_episode['jpg'], caption=caption)
                session.query(LastTVShow).filter(LastTVShow.title_ru == old_episode).\
                    update({
                        'title_en': new_episode['title_en'],
                        'title_ru': new_episode['title_ru'],
                        'jpg': new_episode['jpg'],
                        'date': dateparser.parse(new_episode['date']),
                        'season': new_episode['season'],
                        'tv_show_link': new_episode['tv_show_link'],
                        'episode_link': new_episode['episode_link'],
                    }, synchronize_session=False)
        session.commit()
        print('update epsiodes')
    else:
        bot.send_message(chat_id=219915673, text='Нет новых серий', disable_notification=True)
        print('Not new episodes')
#print(set([json.loads(episode)['title_ru'] for episode in episodes_in_db]))
#print(json.loads(episodes_in_db))
#print(new_episodes[0])