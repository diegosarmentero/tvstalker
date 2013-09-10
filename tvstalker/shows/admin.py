# -*- coding: utf-8 -*-
from django.contrib import admin

from shows import models


class TvDbApiAdmin(admin.ModelAdmin):
    list_display = ('key',)
    list_filter = ('key',)


class GenreTagsAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    list_filter = ('genre',)


class ShowAdmin(admin.ModelAdmin):
    list_display = ('showid', 'title', 'overview', 'showid', 'dayofweek',
        'poster', 'current', 'rated', 'lastupdate')
    list_filter = ('showid', 'title', 'overview', 'showid', 'dayofweek',
        'poster', 'current', 'rated', 'lastupdate')


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('showid', 'nro')
    list_filter = ('showid', 'nro')


class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        'showid', 'season_nro', 'nro', 'name', 'overview', 'airdate')
    list_filter = ('showid', 'season_nro', 'nro', 'name', 'overview', 'airdate')


class ShowNotFoundAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('showid', 'show', 'user')
    list_filter = ('showid', 'show', 'user')


admin.site.register(models.TvDbApi, TvDbApiAdmin)
admin.site.register(models.GenreTags, GenreTagsAdmin)
admin.site.register(models.Show, ShowAdmin)
admin.site.register(models.Season, SeasonAdmin)
admin.site.register(models.Episode, EpisodeAdmin)
admin.site.register(models.ShowNotFound, ShowNotFoundAdmin)
admin.site.register(models.UserFollowing, UserFollowingAdmin)
