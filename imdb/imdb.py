# -*- coding: utf-8 -*-

import os

from BeautifulSoup import BeautifulSoup

import browser


class NotGoodMatchException(Exception):
    """Not Good Match Exception."""


class Imdb(object):

    imdb_link = 'http://www.imdb.com%s'
    query = 'http://www.imdb.com/find?q=%s&s=tt'

    def __init__(self):
        self._browser = browser.Browser()
        self.data = {}
        self.title = ''
        root_path = os.path.dirname(os.path.dirname(__file__))
        self.download_path = os.path.join(root_path, 'static', 'img', 'shows')

    def search(self, title):
        self.title = title.lower()
        search = self.query % self.title.replace(' ', '+')
        page = self._browser.open(search)
        content = page.read()
        try:
            start = content.index('<p><b>Popular Titles</b>')
            end_string = '</table> </p>'
            end = content[start:].index(end_string) + len(end_string)
            content = content[start:start + end]
            soup = BeautifulSoup(content)
            table = soup.find('table')
            link = table.find('a')['href']
            self._load_show_data(link)
        except ValueError:
            #do something
            pass

    def _load_show_data(self, link):
        link = self.imdb_link % link
        page = self._browser.open(link)
        content = page.read()
        soup = BeautifulSoup(content)
        if (self.title not in repr(soup.title).lower() or
            'tv serie' not in repr(soup.title).lower()):
            raise NotGoodMatchException(self.title)

        div = soup.find('div', id="title-overview-widget")
        self.data['image_link'] = div.find('img')['src']
        self.data['description'] = div.find('p', itemprop='description').text
        self.title = self.title.title()
        #self._download_image()
        #self._load_calendar(link)

    def _load_calendar(self, link):
        episodes_link = link + 'episodes'
        page = self._browser.open(episodes_link)
        content = page.read()
        soup = BeautifulSoup(content)
        season_list = soup.find('select', id='bySeason')
        values = season_list.findAll('option')
        seasons = [int(i.text) for i in values]
        self.data['seasons'] = seasons

        self._parse_season(seasons[-1], content)
        for season in seasons[:-1]:
            page = self._browser.open(episodes_link)
            content = page.read()
            self._parse_season(season, content)

    def _parse_season(self, nro, content):
        soup = BeautifulSoup(content)

    def _download_image(self):
        img = self._browser.open(self.data['image_link']).read()
        # store img