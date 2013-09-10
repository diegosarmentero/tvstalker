# -*- coding: utf-8 -*-
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
            result = self.parse_show(search[0])
        elif len(search) == 0:
            result = self.inform_error(title)
        else:
            result = self.parse_shows_results(search)
        return result

    def get_show_by_id(self, showid):
        show = self.db.get(showid, "en")
        return self.parse_show(show)

    def parse_show(self, show):
        show.update()

        # return if lastupdated is the same

        # Get Show
        showdb, created = models.Show.objects.get_or_create(showid=show.id)
        if created:
            showdb.title = show.SeriesName
            showdb.overview = show.Overview
            showdb.dayofweek = show.Airs_DayOfWeek
            showdb.current = show.Status == 'Continuing'
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