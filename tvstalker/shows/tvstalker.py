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

    def get_show(self, title):
        search = self.db.search(title, "en")
        result = None
        if len(search) == 1:
            result = self.parse_show(search[0], title)
        elif len(search) == 0:
            result = self.inform_error(title)
        else:
            result = self.parse_shows_results(search)
        return result

    def get_show_by_id(self, showid):
        show = self.db.get(showid, "en")
        return self.parse_show(show)

    def parse_show(self, show, title=""):
        #check if already follow
        try:
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

                data = {}
                data["poster"] = showdb.poster
                data["showid"] = showdb.showid
                data["title"] = showdb.title
                self.get_episode_info_by_date(showdb, data)
                return data
            else:
                data = {"do_nothing": True}
                data["poster"] = showdb.poster
                data["showid"] = showdb.showid
                data["title"] = showdb.title
                self.get_episode_info_by_date(showdb, data)
                return data
        except:
            return {"error": "Error, please try again later..."}

    def get_episode_info_by_date(self, showdb, data):
        today = datetime.date.today()
        result = models.Episode.objects.filter(showid=showdb.showid,
            airdate__gte=datetime.date.today()).order_by('airdate')
        if len(result) > 0:
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

    def parse_shows_results(self, shows):
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

    def inform_error(self, title):
        shownot, created = models.ShowNotFound.objects.get_or_create(name=title)
        if created:
            shownot.save()
        return {"error": "Tv Show couldn't be found..."}

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