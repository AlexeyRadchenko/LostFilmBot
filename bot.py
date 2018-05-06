from conf import TOKEN, SOCKS_USER, SOCKS_PASS, SOCKS_URL, UPDATER_TASK_TIMER
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, RegexHandler
from bot_commands import start, help, check, spy, updater_task, settings, timezone_set, silent_time


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    socks_kwargs = {'proxy_url': SOCKS_URL, 'urllib3_proxy_kwargs': {
        'username': SOCKS_USER, 'password': SOCKS_PASS, 'timeout': 2}}

    updater = Updater(token=TOKEN, request_kwargs=socks_kwargs)
    dispatcher = updater.dispatcher
    #tasks = updater.job_queue
    """run updates every 15 minutes(900 seconds) after start (param first=0)"""
    #tasks.run_repeating(updater_task, interval=UPDATER_TASK_TIMER, first=0)

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    settings_handler =CommandHandler('settings', settings)
    check_handler = CommandHandler('check', check)
    spy_handler = CommandHandler('spy', spy)

    check_reg_handler = RegexHandler(r'Новинки', check)
    settings_reg_handler = RegexHandler(r'Настройка уведомлений', settings)
    timezone_set_reg_handler = RegexHandler(r'Europe/\w+|Asia/\w+', timezone_set)
    silent_time_reg_handler = RegexHandler(r'\d{1,2}-\d{1,2}', silent_time)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(check_handler)
    dispatcher.add_handler(spy_handler)
    dispatcher.add_handler(settings_reg_handler)
    dispatcher.add_handler(timezone_set_reg_handler)
    dispatcher.add_handler(silent_time_reg_handler)
    dispatcher.add_handler(check_reg_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
