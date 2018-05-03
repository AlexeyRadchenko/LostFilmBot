from conf import TOKEN, SOCKS_USER, SOCKS_PASS, SOCKS_URL
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from bot_commands import start, help, check, spy
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
socks_kwargs = {'proxy_url': SOCKS_URL, 'urllib3_proxy_kwargs': {
    'username': SOCKS_USER, 'password': SOCKS_PASS, 'timeout': 2}}

updater = Updater(token=TOKEN, request_kwargs=socks_kwargs)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
check_handler = CommandHandler('check', check)
spy_handler = CommandHandler('spy', spy)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(check_handler)
dispatcher.add_handler(spy_handler)


updater.start_polling()
