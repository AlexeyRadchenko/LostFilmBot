from datetime import datetime
from pytz import timezone
import pytz
OFFSET = 127462 - ord('A')

def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

def get_new_episode(episode_title, episodes):
    for i, episode in enumerate(episodes, start=0):
        if episode['title_ru'] == episode_title:
            return episode


def notification(usertime):
    return usertime

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

#print(notification(datetime(2018, 5, 4, 14, 53, 18)))
#now = datetime.now(timezone('Europe/Yekaterinburg'))
#print(now)
#print(notification(datetime.now(tz=timezone('Europe/Amsterdam'))))


