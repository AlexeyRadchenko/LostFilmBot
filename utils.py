from datetime import datetime
from pytz import timezone
from database.models import UserProfile
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.error import Unauthorized


OFFSET = 127462 - ord('A')


def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


def get_new_episode(episode_title, episodes):
    for i, episode in enumerate(episodes, start=0):
        if episode['title_ru'] == episode_title:
            return episode


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def main_menu_keyboard(user_db, update=None, session=None):
    if not user_db:
        db_object = UserProfile(
            chat_id=update.message.chat_id,
            notify_sound=True,
            spy=False,
            notify_timer=False
        )
        session.add(db_object)
        session.commit()
        status_notifications = emojize(':no_entry_sign:', use_aliases=True)
        status_sound = emojize(":white_check_mark:", use_aliases=True)
        status_timer = emojize(':no_entry_sign:', use_aliases=True)
    else:
        if user_db.spy:
            status_notifications = emojize(":white_check_mark:", use_aliases=True)
        else:
            status_notifications = emojize(':no_entry_sign:', use_aliases=True)

        if user_db.notify_sound:
            status_sound = emojize(":white_check_mark:", use_aliases=True)
        else:
            status_sound = emojize(':no_entry_sign:', use_aliases=True)

        if user_db.notify_timer:
            status_timer = emojize(":white_check_mark:", use_aliases=True)
        else:
            status_timer = emojize(':no_entry_sign:', use_aliases=True)

    button_list = [
        [KeyboardButton('Новинки'), KeyboardButton('Уведомления ' + status_notifications)],
        [KeyboardButton('Настройка расписания уведомлений ' + status_timer)],
        [KeyboardButton('Звук уведомлений ' + status_sound)]
    ]
    return ReplyKeyboardMarkup(button_list, resize_keyboard=True)


def sound_check(user):
    if not user.notify_sound:
        return False
    else:
        if user.time_notify_start and user.timezone:
            pass


def hour_format_check(hour):
    if 0 <= int(hour) < 24:
        return True
    else:
        return False


def user_list_send(bot, photo, caption, session):
    users_list = session.query(UserProfile).filter(UserProfile.spy).all()
    for user in users_list:
        try:
            if user.notify_sound or user.notify_timer:
                now = datetime.now(timezone(user.timezone)).time()
                if now >= user.time_notify_start or now <= user.time_notify_stop:
                    bot.sendPhoto(chat_id=user.chat_id, photo=photo, caption=caption, disable_notification=True)
                else:
                    bot.sendPhoto(chat_id=user.chat_id, photo=photo, caption=caption)
            else:
                bot.sendPhoto(chat_id=user.chat_id, photo=photo, caption=caption, disable_notification=True)
        except Unauthorized:
            session.query(UserProfile).filter(UserProfile.chat_id == user.chat_id).delete()
            session.commit()
