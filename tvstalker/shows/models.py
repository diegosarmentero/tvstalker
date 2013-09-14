from django.db import models
from django.contrib.auth.models import User


class TvDbApi(models.Model):
    key = models.CharField(max_length=200)


class GenreTags(models.Model):
    genre = models.CharField(max_length=200)


class Episode(models.Model):
    showid = models.IntegerField()
    season_nro = models.IntegerField(default=0)
    nro = models.IntegerField(default=0)
    name = models.CharField(max_length=200, default="")
    overview = models.TextField(blank=True, null=True)
    airdate = models.DateField(null=True)


class Season(models.Model):
    showid = models.IntegerField()
    nro = models.IntegerField(default=0)
    episodes = models.ManyToManyField(Episode, null=True)


class Show(models.Model):
    """ Represents a TV show."""
    showid = models.IntegerField(unique=True)
    title = models.CharField(max_length=200, default="")
    overview = models.TextField(blank=True, default="")
    dayofweek = models.CharField(max_length=20, null=True)
    genre = models.ManyToManyField(GenreTags, null=True)
    poster = models.URLField(null=True)
    current = models.BooleanField(default=False)
    rated = models.IntegerField(default=0)
    lastupdate = models.DateField(auto_now=True)
    seasons = models.ManyToManyField(Season, null=True)


class UserFollowing(models.Model):
    showid = models.IntegerField()
    show = models.ForeignKey(Show, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class UserViewedEpisodes(models.Model):
    showid = models.IntegerField()
    season = models.IntegerField(default=0)
    episode = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    viewed = models.BooleanField(default=False)


class ShowNotFound(models.Model):
    name = models.CharField(max_length=200, unique=True)