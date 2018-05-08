from conf import TOKEN, SOCKS5_ARGS, UPDATER_TASK_TIMER
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, RegexHandler
from bot_commands import (start, help, check,
                          spy, updater_task, settings,
                          timezone_set, silent_time, notifications_timer_on_off,
                          set_notifications, sound_notifications_mute)


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
        RegexHandler(r'Включить расписание|Выключить расписание', notifications_timer_on_off),
        RegexHandler(r'Настроить расписание|Изменить настройки', set_notifications),
        RegexHandler(r'Звук уведомлений', sound_notifications_mute)
    ]

    append_handlers(dispatcher, command_handlers)
    append_handlers(dispatcher, regexp_command_handlers)

    tasks.run_repeating(updater_task, interval=UPDATER_TASK_TIMER, first=0)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
