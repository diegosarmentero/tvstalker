# -*- coding: utf-8 -*-
import datetime

from pytvdbapi import api

from shows import models

TVDB_KEY = ''


def get_key():
    global TVDB_KEY

    keys = models.TvDbApi.objects.values_list('key', flat=True)
    TVDB_KEY = keys[0]


# SET THE KEY VALUE
get_key()


class TvStalker(object):

    def __init__(self):
        self.db = api.TVDB(TVDB_KEY, banners=True)

    def get_show(self, title, user=None, client=False):
        search = self.db.search(title, "en")
        result = None
        if len(search) == 1:
            result = self.parse_show(search[0], user, title, client)
        elif len(search) == 0:
            result = self.inform_error(title)
        else:
            result = self.parse_shows_results(search)
        return result

    def get_show_by_id(self, showid, user=None, client=False):
        try:
            show = self.db.get(showid, "en")
            return self.parse_show(show, user, client)
        except:
            return {"error": "Error, please try again later..."}

    def parse_show(self, show, user, title="", client=False):
        try:
            data = {}
            if user:
                follow, created = models.UserFollowing.objects.get_or_create(
                    showid=show.id, user=user)
                if not created:
                    data["do_nothing"] = True
                    return data
            show.update()

            # Get Show
            showdb, created = models.Show.objects.get_or_create(showid=show.id)
            if created:
                showdb.title = show.SeriesName
                showdb.overview = show.Overview
                showdb.dayofweek = show.Airs_DayOfWeek
                showdb.current = show.Status == 'Continuing'
                if show.Rating:
                    showdb.rated = int(show.Rating)
                posters = [b for b in show.banner_objects
                            if b.BannerType == "poster"]
                if len(posters) > 0:
                    showdb.poster = posters[0].banner_url
                showdb.save()
                # Genre
                for genre in show.Genre:
                    genredb, gcreate = models.GenreTags.objects.get_or_create(
                        genre=genre)
                    if gcreate:
                        genredb.save()
                        showdb.genre.add(genredb)
                for season in show:
                    self.save_season(season, showdb)

                data["poster"] = showdb.poster
                data["showid"] = showdb.showid
                data["title"] = showdb.title
                if client:
                    data["dayOfWeek"] = showdb.dayofweek
                    data["current"] = showdb.current
                    self.get_episode_info_by_date_client(showdb, data)
                else:
                    self.get_episode_info_by_date(showdb, data)
            else:
                data["poster"] = showdb.poster
                data["showid"] = showdb.showid
                data["title"] = showdb.title
                if client:
                    data["dayOfWeek"] = showdb.dayofweek
                    data["current"] = showdb.current
                    self.get_episode_info_by_date_client(showdb, data)
                else:
                    self.get_episode_info_by_date(showdb, data)
            # Set Following
            if user:
                follow.show = showdb
                follow.save()
            return data
        except:
            return {"error": "Error, please try again later..."}

    def get_episode_info_by_date(self, showdb, data, date=None):
        ok = False
        today = datetime.date.today()
        if date is None:
            result = models.Episode.objects.filter(showid=showdb.showid,
                airdate__gte=today).order_by('airdate')
        else:
            result = models.Episode.objects.filter(showid=showdb.showid,
                airdate=date).order_by('airdate')
        if len(result) > 0:
            ok = True
            data["season_nro"] = result[0].season_nro
            data["episode_nro"] = result[0].nro
            if result[0].airdate == today:
                data["next"] = "TODAY"
                data["airdate"] = ""
            else:
                data["next"] = "Next Episode"
                data["airdate"] = str(result[0].airdate)
        elif showdb.current:
            data["season_nro"] = "tbd"
            data["episode_nro"] = "tbd"
            data["next"] = ""
            data["airdate"] = ""
        else:
            result = models.Episode.objects.filter(
                showid=showdb.showid).exclude(
                    season_nro=0).order_by('-airdate')
            if len(result) > 0:
                data["season_nro"] = result[0].season_nro
                data["episode_nro"] = result[0].nro
                data["next"] = "Last Episode"
                if result[0].airdate:
                    data["airdate"] = str(result[0].airdate)
                else:
                    data["airdate"] = "Unknown"
            else:
                data["season_nro"] = 0
                data["episode_nro"] = 0
                data["next"] = "Last Episode"
                data["airdate"] = "Unknown"
        return ok

    def parse_shows_results(self, shows):
        try:
            data = {}
            data["multiple"] = len(shows)
            info = []
            for show in shows:
                show.update()
                posters = [b for b in show.banner_objects
                            if b.BannerType == "poster"]
                poster = ''
                if len(posters) > 0:
                    poster = posters[0].banner_url
                info.append([show.id, show.SeriesName, poster])
            data["shows"] = info
            return data
        except:
            return {"error": "Error, please try again later..."}

    def inform_error(self, title):
        shownot, created = models.ShowNotFound.objects.get_or_create(name=title)
        if created:
            shownot.save()
        return {"error": "Tv Show: '%s' couldn't be found..." % title}

    def save_season(self, season, show):
        nro = season.season_number
        seasondb, created = models.Season.objects.get_or_create(
            showid=show.showid, nro=nro)
        if created:
            seasondb.save()
            show.seasons.add(seasondb)
            for episode in season:
                self.save_episode(episode, seasondb)

    def save_episode(self, episode, season):
        nro = episode.EpisodeNumber
        episodedb, created = models.Episode.objects.get_or_create(
            showid=season.showid, season_nro=season.nro, nro=nro)
        if created:
            episodedb.name = episode.EpisodeName
            episodedb.overview = episode.Overview
            if episode.FirstAired:
                episodedb.airdate = episode.FirstAired
            episodedb.save()
            season.episodes.add(episodedb)

    def get_episode_info_by_date_client(self, showdb, data, date=None):
        ok = False
        today = datetime.date.today()
        if date is None:
            result = models.Episode.objects.filter(showid=showdb.showid,
                airdate__gte=today).order_by('airdate')
        else:
            result = models.Episode.objects.filter(showid=showdb.showid,
                airdate=date).order_by('airdate')
        if len(result) > 0:
            ok = True
            data["season_nro"] = str(result[0].season_nro)
            data["episode_nro"] = str(result[0].nro)
            data["date"] = str(result[0].airdate)
            if result[0].airdate == today:
                data["next"] = "TODAY"
                data["airdate"] = ""
            else:
                data["next"] = "Next Episode"
                data["airdate"] = str(result[0].airdate)
        elif showdb.current:
            data["season_nro"] = "tbd"
            data["episode_nro"] = "tbd"
            data["next"] = ""
            data["airdate"] = ""
        else:
            result = models.Episode.objects.filter(
                showid=showdb.showid).exclude(
                    season_nro=0).order_by('-airdate')
            if len(result) > 0:
                data["season_nro"] = str(result[0].season_nro)
                data["episode_nro"] = str(result[0].nro)
                data["next"] = "Last Episode"
                data["date"] = str(result[0].airdate)
                if result[0].airdate:
                    data["airdate"] = str(result[0].airdate)
                else:
                    data["airdate"] = "Unknown"
            else:
                data["season_nro"] = "0"
                data["episode_nro"] = "0"
                data["next"] = "Last Episode"
                data["airdate"] = "Unknown"
        return ok