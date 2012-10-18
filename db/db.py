# -*- coding: utf-8 -*-

import model


def get_tv_show(title):
    serie = model.Serie.all()
    serie.filter('name =', title)
    if serie.count() == 0:
        return None
    return serie[0]