# -*- coding: utf-8 -*-

from shows import tvstalker


tv = tvstalker.TvStalker()


def get_show(title):
    return tv.get_show(title)


def get_show_by_id(showid):
    return tv.get_show_by_id(showid)