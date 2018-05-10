# ////////////////////////////////////BOT-SETTINGS/////////////////////////////////////////////////////////////////////
TOKEN = 'bot_token'

"""socks5h {h} - need dns resolve on socks server, else api.telegram.org connections error """
WEB_HOOK_DOMAIN = f'https://site.bot/{TOKEN}'
# CERT_PEM = 'cert.pem'

# if need socks5
SOCKS5_ARGS = None
"""
SOCKS5_ARGS = {
    'proxy_url': 'socks5h://127.0.0.1:1234/',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'login',
        'password': 'pass',
        'timeout': 1
    }
}
"""

"""if DEBUG = True creating LFbot.db in root, using sqlite3. If False using postgresql and DB_CONNECT params"""
DEBUG = True
DB_CONNECT = 'postgresql+psycopg2://user:pass@localhost/bot_data_base'
# /////////////////////////////////////TEXT-MESSAGES-FOR-BOT-COMMANDS//////////////////////////////////////////////////

"""required {} - username"""
START_TEXT = 'Привет, {}. ' \
             'Я бот, который сообщает о новых сериалах и новых эпизодах на Lostfilm.tv\n' \
             'Для вызова справки\nнапиши /help'

HELP_TEXT = {
    'main': 'Вот список моих команд :\n'
            '/help - справка\n'
            '/check или клавиша "Новинки" - проверить раздел новинки на LostFilm\n'
            '/spy или клавиша "Уведомления" - '
            '(Вкл./Выкл.) бот будет автоматически следить за появлением новых эпизодов\n'
            '/settings или клавиша "Настройка уведомлений" - настройка и включение/выключение периода времени, '
            'в течении которого уведомления будут приходить беззвучно\n'
            '/sound или клавиша "Звук уведомлений" - '
            'включает или выключает звук автоуведомлений независимо от расписания',
    'timezone': 'Укажите время когда автоуведомления должны быть без звука.'
                'Часы указывайте от 0 до 23, в формате ЧАС-ЧАС (пример: 11-9)\n'
                'Например команда "23-8"  означает, что уведомления будут приходить без звука с 23 часов ночи до 8 утра'
}

AFTER_CHECK_TEXT = 'Последние новинки'

"""{0} - название сериала, {1} - название серии, {2} - ссылка на описание сериала"""
EPISODE_CAPTION = '{0} - {1}\nО сериале: {2}'
# ////////////////////////////////////END-TEXT-MESSAGES////////////////////////////////////////////////////////////////

# ////////////////////////////////////TIMERS-OF-SHEDULED-TASKS/////////////////////////////////////////////////////////
"""run updates every 15 minutes(900 seconds) after start (param first=0)"""
UPDATER_TASK_TIMER = 900
# ////////////////////////////////////END-TIMERS-OF-SHEDULED-TASKS////////////////////////////////////////////////////
"""gist with python timezones https://gist.github.com/pamelafox/986163"""
PY_TIMEZONES_RU = {'timezones': [
    'Europe/Kaliningrad',
    'Europe/Moscow',
    'Europe/Volgograd',
    'Europe/Samara',
    'Asia/Yekaterinburg',
    'Asia/Omsk',
    'Asia/Novosibirsk',
    'Asia/Krasnoyarsk',
    'Asia/Irkutsk',
    'Asia/Yakutsk',
    'Asia/Vladivostok',
    'Asia/Sakhalin',
    'Asia/Magadan',
    'Asia/Kamchatka',
    'Asia/Anadyr'
    ],
    'code': 'RU', 'continent': 'Europe', 'name': 'Russia', 'capital': 'Moscow'}
