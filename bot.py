from conf import TOKEN, SOCKS5_ARGS, UPDATER_TASK_TIMER
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, RegexHandler
from bot_commands import (start, help, check,
                          spy, updater_task, settings,
                          timezone_set, silent_time, notifications_timer_on,
                          notifications_timer_off, set_notifications, sound_notifications_mute)


def append_handlers(dispatcher, handlers_list):
    for handler in handlers_list:
        dispatcher.add_handler(handler)


def append_error_handlers(dispatcher, handlers_list):
    for handler in handlers_list:
        dispatcher.add_error_handler(handler)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater = Updater(token=TOKEN, request_kwargs=SOCKS5_ARGS)
    dispatcher = updater.dispatcher
    tasks = updater.job_queue

    command_handlers = [
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('settings', settings),
        CommandHandler('check', check),
        CommandHandler('spy', spy)
    ]

    regexp_command_handlers = [
        RegexHandler(r'Новинки', check),
        RegexHandler(r'Настройка расписания уведомлений', settings),
        RegexHandler(r'Europe/\w+|Asia/\w+', timezone_set),
        RegexHandler(r'\d{1,2}-\d{1,2}', silent_time),
        RegexHandler(r'\bУведомления\s', spy),
        RegexHandler(r'Меню', start),
        RegexHandler(r'Включить расписание', notifications_timer_on),
        RegexHandler(r'Выключить расписание', notifications_timer_off),
        RegexHandler(r'Настроить расписание|Изменить настройки', set_notifications),
        RegexHandler(r'Звук уведомлений', sound_notifications_mute)
    ]

    append_handlers(dispatcher, command_handlers)
    append_handlers(dispatcher, regexp_command_handlers)

    """run updates every 15 minutes(900 seconds) after start (param first=0)"""
    tasks.run_repeating(updater_task, interval=UPDATER_TASK_TIMER, first=0)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

"""
    start_handler = 
    help_handler = 
    settings_handler = 
    check_handler =


    check_reg_handler = 
    settings_reg_handler = 
    timezone_set_reg_handler = 
    silent_time_reg_handler = 
    spy_reg_handler = 
    main_menu_reg_handler = 
    notifications_tm_on = 
    notifications_tm_off = 
    notifications_tm_set =

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(check_handler)
    dispatcher.add_handler(spy_handler)
    dispatcher.add_handler(settings_reg_handler)
    dispatcher.add_handler(timezone_set_reg_handler)
    dispatcher.add_handler(silent_time_reg_handler)
    dispatcher.add_handler(check_reg_handler)
    dispatcher.add_handler(spy_reg_handler)
    dispatcher.add_handler(main_menu_reg_handler)
    dispatcher.add_handler(notifications_tm_on)
    dispatcher.add_handler(notifications_tm_off)
    dispatcher.add_handler(notifications_tm_set)
    dispatcher.add_error_handler(error_callback)"""
