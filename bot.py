from conf import TOKEN, SOCKS_USER, SOCKS_PASS
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
socks_kwargs = {'proxy_url': 'socks5://188.166.167.217:7953/', 'urllib3_proxy_kwargs': {
    'username': SOCKS_USER, 'password': SOCKS_PASS, 'timeout': 2}}
updater = Updater(token=TOKEN, request_kwargs=socks_kwargs)
dispatcher = updater.dispatcher


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

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
