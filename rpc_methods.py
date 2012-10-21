# -*- coding: utf-8 -*-

import imdb
from db import (
    db,
    model,
)


class RPCMethods(object):

    def AddTvShow(self, *args, **kwargs):
        data = {}
        try:
            title = imdb.get_show_info(args[0])
            show = db.get_tv_show(title)
            user = kwargs['user']
            if show and user:
                following = model.FollowingShows()
                following.login = user
                following.serie = show
                following.put()
                data['']
        except Exception, reason:
            data['error'] = str(reason)
        return data
