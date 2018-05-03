from parser.parser import LostFilmParser


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
    new_episodes = LostFilmParser().get_new_shows_episodes()
    for episode in new_episodes:
        caption = '{0} - {1}\nО сериале:'.format(episode['title_ru'], episode['season'])
        bot.sendPhoto(chat_id=update.message.chat_id, photo=episode['jpg'], caption=caption)
    bot.send_message(chat_id=update.message.chat_id, text='ok')


def spy(bot, update):
    pass