# -*- coding: utf-8 -*-

import os

from BeautifulSoup import BeautifulSoup

from db import (
    db,
    model,
)
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
        return self.title

    def _load_show_data(self, link):
        link = self.imdb_link % link
        show = db.is_show_in_db(link)
        if show:
            self.title = show.name
            return
        page = self._browser.open(link)
        content = page.read()
        soup = BeautifulSoup(content)
        if (self.title not in repr(soup.title).lower() or
            'tv serie' not in repr(soup.title).lower()):
            raise NotGoodMatchException(self.title)

        div = soup.find('div', id="title-overview-widget")
        self.data['image_link'] = div.find('img')['src']
        self.data['description'] = div.find('p', itemprop='description').text
        serie = model.Serie()
        serie.name = self.title
        serie.title = self.title.title()
        serie.description = self.data['description']
        serie.store_image(self.data['image_link'])
        serie.source_url = link
        serie.put()
        self._load_calendar(serie, link)

    def _load_calendar(self, serie, link):
        episodes_link = link + 'episodes'
        page = self._browser.open(episodes_link)
        content = page.read()
        soup = BeautifulSoup(content)
        season_list = soup.find('select', id='bySeason')
        values = season_list.findAll('option')
        seasons = [int(i.text) for i in values]
        self.data['seasons'] = seasons

        # Update last season
        serie.last_season = seasons[-1]
        serie.put()
        # Obtain Seasons
        season = model.Season()
        season.nro = seasons[-1]
        season.put()
        self._parse_season(season, content)
        # This produce a timeout, maybe could be completed on demand
        #for season_nro in seasons[:-1]:
            #epi_link = episodes_link + '?season=%s' % season_nro
            #page = self._browser.open(epi_link)
            #content = page.read()
            #season = model.Season()
            #season.nro = season_nro
            #season.put()
            #self._parse_season(season, content)

    def _parse_season(self, season, content):
        soup = BeautifulSoup(content)
        divs = soup.findAll('div', id='episodes')
        for div in divs:
            airdate = div.find('div', {'class': 'airdate'}).text
            title = div.find('a', itemprop='name').text
            description = div.find('a', itemprop='description').text
            episode = model.Episode()
            episode.title = title
            episode.description = description
            real_date = self._obtain_airdate(airdate)
            episode.airdate = real_date
            episode.season = season
            episode.put()

    def _obtain_airdate(self, airdate):
        pass
