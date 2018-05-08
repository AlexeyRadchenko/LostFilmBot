from parser.parser import LostFilmParser
from database.database_init import engine_selector
from database.models import LastTVShow, UserProfile
import dateparser
import conf
from utils import get_new_episode, build_menu, flag, main_menu_keyboard, user_list_send, hour_format_check
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from datetime import datetime
from re import search


engine, Session = engine_selector()
session = Session()


def start(bot, update):
    username = update.message.chat.first_name
    user_db = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    reply_markup = main_menu_keyboard(user_db, update=update, session=session)
    bot.send_message(chat_id=update.message.chat_id, text=conf.START_TEXT.format(username), reply_markup=reply_markup)


def help(bot, update):
    print(update.message)
    bot.send_message(chat_id=update.message.chat_id, text=conf.HELP_TEXT)


def settings(bot, update):
    status, reply_markup = None, None
    user = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    if user.notify_timer:
        status = f'Расписание включено: часовой пояс {user.timezone}, звук уведомлений отключен с {user.time_notify_start} до {user.time_notify_stop}'
        button_list = [
            [KeyboardButton("Выключить расписание"), KeyboardButton("Изменить настройки")],
            [KeyboardButton("Меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    elif not user.notify_timer and not user.time_notify_start:
        status = 'Расписание не включено и не настроено'
        button_list = [
            KeyboardButton("Настроить расписание"),
            KeyboardButton("Меню")
        ]
        reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True)
    elif not user.notify_timer:
        status = f'Раписание выключено: часовой пояс {user.timezone}, звук уведомлений отключен с {user.time_notify_start} до {user.time_notify_stop}'
        button_list = [
            [KeyboardButton("Включить расписание"), KeyboardButton("Изменить настройки")],
            [KeyboardButton("Меню")]
        ]
        reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text=status, reply_markup=reply_markup)


def notifications_timer_on_off(bot, update):
    user = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    if not user.notify_timer:
        user.notify_timer = True
        reply_markup = main_menu_keyboard(user)
        bot.send_message(chat_id=update.message.chat_id, text='Расписание включено', reply_markup=reply_markup)
    else:
        user.notify_timer = False
        reply_markup = main_menu_keyboard(user)
        bot.send_message(chat_id=update.message.chat_id, text='Расписание выключено', reply_markup=reply_markup)
    session.commit()


def set_notifications(bot, update):
    button_list = [KeyboardButton(timezone) for timezone in conf.PY_TIMEZONES_RU['timezones']]
    button_list.append(KeyboardButton('Меню'))
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=3), resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Выберите часовой пояс", reply_markup=reply_markup)


def timezone_set(bot, update):
    try:
        timezone = search(r'Europe/\w+|Asia/\w+', update.message.text).group()
    except AttributeError:
        timezone = None
    if timezone:
        session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).update(
            {
                'timezone': timezone,
            },
            synchronize_session=False
        )
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Укажите время когда сообщения должны быть без звука в 24-х часовом формате, пример 23-8 (с 23 ночи до 8 часов сообения будут беззвучными)", reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Неверный формат часового пояса')


def silent_time(bot, update):
    user = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    try:
        start_time, stop_time = search(r'\d{1,2}-\d{1,2}', update.message.text).group().split('-')
    except AttributeError:
        start_time, stop_time = None, None
    if hour_format_check(start_time) and hour_format_check(stop_time) and user.timezone:
        start_time = datetime.strptime(f'{start_time}:00:00', "%H:%M:%S").time()
        stop_time = datetime.strptime(f'{stop_time}:00:00', "%H:%M:%S").time()
        user.time_notify_start = start_time
        user.time_notify_stop = stop_time
        user.notify_timer = True
        """session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).update(
            {
                'time_notify_start': start_time,
                'time_notify_stop': stop_time
            },
            synchronize_session=False
        )"""
        session.commit()
        reply_markup = main_menu_keyboard(user)
        bot.send_message(chat_id=update.message.chat_id, text=f'Расписание включено. Звук автоматических уведомлений отключен с {start_time.hour}:00 до {stop_time.hour}:00', reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Неверный формат /help')


def sound_notifications_mute(bot, update):
    user = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    if user.notify_sound:
        user.notify_sound = False
        session.commit()
        reply_markup = main_menu_keyboard(user)
        bot.send_message(chat_id=update.message.chat_id, text='Звук отключен', reply_markup=reply_markup)
    else:
        user.notify_sound = True
        session.commit()
        reply_markup = main_menu_keyboard(user)
        bot.send_message(chat_id=update.message.chat_id, text='Звук включен', reply_markup=reply_markup)


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
        spam = False
        session.commit()
    else:
        last_check = user_db.__dict__['when_check']
        current_check = datetime.now()
        delta = current_check - last_check
        print(current_check, last_check, delta.seconds)
        if delta.seconds >= 60:
            session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).update(
                {
                    'when_check': current_check
                }
            )
            spam = False
            session.commit()
        else:
            spam = True

    if not episodes_in_db and not spam:
        for episode in episodes_in_request:
            caption = conf.EPISODE_CAPTION.format(
                episode['title_ru'], episode['season'], episode['tv_show_link'])
            bot.sendPhoto(chat_id=update.message.chat_id,
                          photo=episode['jpg'], caption=caption, disable_notification=True
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
    elif not spam:
        for episode in episodes_in_request:
            caption = conf.EPISODE_CAPTION.format(
                episode['title_ru'], episode['season'], episode['tv_show_link'])
            bot.sendPhoto(chat_id=update.message.chat_id, photo=episode['jpg'], caption=caption, disable_notification=True)
        bot.send_message(chat_id=update.message.chat_id, text=conf.AFTER_CHECK_TEXT, disable_notification=True)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Проверить новинки через 1 минуту', disable_notification=True)


def spy(bot, update):
    user = session.query(UserProfile).filter(UserProfile.chat_id == update.message.chat_id).one_or_none()
    if not user.spy:
        user.spy = True
        reply_markup = main_menu_keyboard(user)
        bot.send_message(chat_id=update.message.chat_id, text='Теперь бот будет автоматически уведомлять вас', reply_markup=reply_markup, disable_notification=True)
    else:
        user.spy = False
        reply_markup = main_menu_keyboard(user)
        bot.send_message(chat_id=update.message.chat_id, text='Уведомления отключены', reply_markup=reply_markup, disable_notification=True)
    session.commit()


def updater_task(bot, job):
    new_episodes = LostFilmParser().get_new_shows_episodes()
    updater_db_session = Session()
    episodes_in_db = updater_db_session.query(LastTVShow).all()
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
                user_list_send(bot, new_episode['jpg'], caption, updater_db_session)
                updater_db_session.query(LastTVShow).filter(LastTVShow.title_ru == old_episode).\
                    update({
                        'title_en': new_episode['title_en'],
                        'title_ru': new_episode['title_ru'],
                        'jpg': new_episode['jpg'],
                        'date': dateparser.parse(new_episode['date']),
                        'season': new_episode['season'],
                        'tv_show_link': new_episode['tv_show_link'],
                        'episode_link': new_episode['episode_link'],
                    }, synchronize_session=False)
        updater_db_session.commit()
    Session.remove()
