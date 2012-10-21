# -*- coding: utf-8 -*-

import datetime

from google.appengine.api import files
from google.appengine.api import images

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
                following = db.is_already_following(user, show)
                if following is None:
                    following = model.FollowingShows()
                    following.login = user
                    following.serie = show
                    following.put()
                else:
                    data['do_nothing'] = True
                    return data
                # Search for recent episode
                episode = db.obtain_most_recent_episode(show)
                data['title'] = show.title
                url = images.get_serving_url(files.blobstore.get_blob_key(
                    show.image_name))
                data['image_url'] = url
                data['season'] = show.last_season
                if episode is not None:
                    data['episode_title'] = episode.title
                    data['episode_nro'] = episode.nro
                    if episode.airdate == datetime.date.today():
                        data['today'] = True
                    else:
                        date = "%s %i, %i" % (
                            episode.airdate.strftime('%B')[:3],
                            episode.airdate.day, episode.airdate.year)
                        data['airdate'] = date
                else:
                    data['episode_title'] = 'N/A'
                    data['episode_nro'] = 'N/A'
                    data['airdate'] = 'N/A'
            else:
                data['error'] = "Tv Show couldn't be found..."
        except Exception, reason:
            data['error'] = str(reason)
        return data
