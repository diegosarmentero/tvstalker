# -*- coding: utf-8 -*-

from db import db
from imdb import Imdb


def get_show_info(title):
    show = db.get_tv_show(title.lower())
    if show:
        return show.name
    imdb = Imdb()
    imdb.search(title)
    return imdb.title