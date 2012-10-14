# -*- coding: utf-8 -*-

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
            self.load_show_data(link)
        except ValueError:
            #do something
            pass

    def load_show_data(self, link):
        link = self.imdb_link % link
        page = self._browser.open(link)
        content = page.read()
        soup = BeautifulSoup(content)
        if self.title not in repr(soup.title).lower():
            raise NotGoodMatchException(self.title)

        self.data['image_link'] = ''
        self.data['description'] = ''
        self.data['genre'] = ''
