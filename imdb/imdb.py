# -*- coding: utf-8 -*-

import os
import difflib
import datetime
import urllib2

from google.appengine.api import urlfetch

from BeautifulSoup import BeautifulSoup

from db import (
    db,
    model,
)


MONTHS = {}

for i in range(1, 13):
    MONTHS[unicode(
        datetime.date(2012, i, 1).strftime('%B').strip().lower())[:3]] = i


class NotGoodMatchException(Exception):
    """Not Good Match Exception."""


class Imdb(object):

    imdb_link = 'http://www.imdb.com%s'
    query = 'http://www.imdb.com/find?q=%s&s=tt'

    def __init__(self):
        self.data = {}
        self.title = ''
        root_path = os.path.dirname(os.path.dirname(__file__))
        self.download_path = os.path.join(root_path, 'static', 'img', 'shows')

    def _search_popular(self, content):
        show_found = False
        try:
            start = content.index('<p><b>Popular Titles</b>')
            end_string = '</table> </p>'
            end = content[start:].index(end_string) + len(end_string)
            soup = BeautifulSoup(content[start:start + end])
            table = soup.find('table')
            for a in table.findAll('a'):
                link = a['href']
                show_found = self._load_show_data(link)
                if show_found:
                    break
        except:
            pass
        return show_found

    def _search_exact_match(self, content):
        show_found = False
        start = content.index('<p><b>Titles (Exact Matches)</b>')
        end_string = '</table> </p>'
        end = content[start:].index(end_string) + len(end_string)
        soup = BeautifulSoup(content[start:start + end])
        table = soup.find('table')
        for a in table.findAll('a'):
            link = a['href']
            show_found = self._load_show_data(link)
            if show_found:
                break
        return show_found

    def search(self, title):
        self.title = title.lower()
        search = self.query % self.title.replace(' ', '+')
        content = urlfetch.Fetch(search, deadline=60,
            allow_truncated=True).content
        try:
            soup = BeautifulSoup(content)
            if soup.link['href'] == 'http://www.imdb.com/find':
                show_found = self._search_popular(content)
                if not show_found:
                    show_found = self._search_exact_match(content)
                if not show_found:
                    raise NotGoodMatchException(self.title)
            else:
                link = soup.find('link', rel='canonical')['href']
                self._load_show_data(link, soup, True)
        except ValueError:
            #do something
            pass
        return self.title

    def _load_show_data(self, link, soup=None, direct=False):
        if soup is None:
            link = self.imdb_link % link
            show = db.is_show_in_db(link)
            if show:
                self.title = show.name
                return True
            content = urlfetch.Fetch(link, deadline=60,
                allow_truncated=True).content
            soup = BeautifulSoup(content)
        page = urllib2.urlopen(link)
        content = page.read(7000)
        title_show = content[content.find('<title>') + 7:
            content.find('</title>') + 8]
        show_title = title_show[:title_show.find(
            '(')].strip().lower()
        if not direct:
            ratio = difflib.SequenceMatcher(None,
                self.title, show_title).ratio()
            matching_name = (ratio < 0.85) and (self.title not in show_title)
            if matching_name or ('tv serie' not in soup.title.text.lower()):
                return False

        div = soup.find('div', id="title-overview-widget")
        img = div.find('img')
        self.data['description'] = div.find('p', itemprop='description').text
        serie = model.Serie()
        self.title = show_title
        serie.name = self.title
        serie.title = self.title.title()
        serie.description = self.data['description']
        if img:
            self.data['image_link'] = img['src']
            serie.store_image(self.data['image_link'])
        serie.source_url = link
        serie.put()
        self._load_calendar(serie, link)
        return True

    def _load_calendar(self, serie, link):
        episodes_link = link + 'episodes'
        content = urlfetch.Fetch(episodes_link, deadline=60,
            allow_truncated=True).content
        soup = BeautifulSoup(content)
        season_list = soup.find('select', id='bySeason')
        if not season_list:
            return
        values = season_list.findAll('option')
        seasons = [int(i.text) for i in values if i and str(i.text).isdigit()]
        self.data['seasons'] = seasons

        # Update last season
        serie.last_season = seasons[-1]
        serie.put()
        # Obtain Seasons
        season = model.Season()
        season.nro = seasons[-1]
        season.serie = serie
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
        divs = soup.findAll('div', itemprop='episodes')
        episode_nro = 1
        for div in divs:
            airdate = div.find('div', {'class': 'airdate'})
            if airdate is None:
                continue
            episode = model.Episode()
            airdate = airdate.text
            title = div.find('a', itemprop='name').text
            episode.title = title
            description = div.find('div', itemprop='description')
            if description is not None:
                episode.description = description.text
            real_date = self._obtain_airdate(airdate)
            episode.airdate = real_date
            episode.season = season
            episode.nro = episode_nro
            episode.put()
            episode_nro += 1

    def _obtain_airdate(self, airdate):
        airdate = airdate.replace('.', '').replace(',', '')
        airdate = airdate.split(' ')
        if len(airdate) != 3:
            return None
        date = datetime.date(int(airdate[2]),
            MONTHS[airdate[0].strip().lower()], int(airdate[1]))
        return date
