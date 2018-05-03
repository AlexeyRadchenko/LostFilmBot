from requests_html import HTMLSession
from re import search
import json
from time import sleep


class LostFilmParser:
    source_url = 'https://www.lostfilm.tv/'
    tv_shows_list_part_url = 'https://www.lostfilm.tv/ajaxik.php'
    part_step = 10

    def __init__(self):
        self.session = HTMLSession()
        self.news_data = self.session.get(self.source_url)

    def get_links(self):
        return self.news_data.html.links

    def get_title_en(self, href):
        try:
            result = search(r'/series/([^/]+)/', href)
            title_en = result.group(1)
            tv_show_link = self.source_url.rstrip('/') + result.group()
        except AttributeError:
            title_en = None
            tv_show_link = None
        return title_en, tv_show_link

    def get_new_shows_episodes(self):
        clear_data = []
        news_block = self.news_data.html.find('.new-movies-block', first=True)
        movies = news_block.find('a.new-movie')
        for movie in movies:
            title_en, show_link = self.get_title_en(movie.attrs['href'])
            clear_data.append(
                {
                    'title_ru': movie.attrs['title'],
                    'title_en': title_en,
                    'jpg': 'http:' + movie.find('img', first=True).attrs['src'],
                    'season': movie.find('.title', first=True).text,
                    'date': movie.find('.date', first=True).text,
                    'episode_link': self.source_url.rstrip('/') + movie.attrs['href'],
                    'tv_show_link': show_link,
                }
            )
        return clear_data

    def load_part_list(self, step):
        url = self.source_url + 'ajaxik.php'
        request_data = self.session.post(
            url=url,
            data={'act': 'serial', 'o': step, 's': 3, 't': 0, 'type': 'search'}
            )
        return json.loads(request_data.content)['data']

    def get_tv_shows_list(self):
        """10->20->30-> пока не вернет пустой список"""
        step = 0
        shows_list = []
        request_result = self.load_part_list(step)
        while request_result:
            for result in request_result:
                shows_list.append(result)
            step += self.part_step
            sleep(1)
            request_result = self.load_part_list(step)
        return shows_list

"""
parser = LostFilmParser()
res = parser.get_tv_shows_list()
print(res[0], len(res))
parser = LostFilmParser()
fast_check = parser.get_new_shows_episodes()
print(fast_check)
"""