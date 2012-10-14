# -*- coding: utf-8 -*-

from imdb import Imdb


def get_show_info(title):
    imdb = Imdb()
    imdb.search(title)