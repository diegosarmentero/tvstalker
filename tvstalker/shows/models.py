from django.db import models


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


class ShowNotFound(models.Model):
    name = models.CharField(max_length=200, unique=True)