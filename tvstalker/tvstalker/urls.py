from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from common import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Login
    (r'^accounts/', include('allauth.urls')),
    # Sections
    url(r'^sign_up/', views.sign_up, name="sign_up"),
    url(r'^about/', views.about, name="about"),
    url(r'^report/', views.report, name="report"),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^details/', views.details, name="details"),
    url(r'^explore/', views.explore, name="explore"),
    url(r'^genres/', views.genres, name="genres"),
    # RPC
    url(r'^rpc/choose_show_guest', views.choose_show_guest,
        name="choose_show_guest"),
    url(r'^rpc/choose_show', views.choose_show, name="choose_show"),
    url(r'^rpc/get_suggestions', views.get_suggestions, name="get_suggestions"),
    url(r'^rpc/guest_load', views.rpc_guest_load, name="rpc_guest_load"),
    url(r'^rpc/guest', views.rpc_guest, name="rpc_guest"),
    url(r'^rpc/mark_as_viewed', views.mark_as_viewed, name="mark_as_viewed"),
    url(r'^rpc/', views.rpc, name="rpc"),
    # Client API
    url(r'^api/get_details', views.get_details, name="get_details"),
    url(r'^api/get_token', views.get_token, name="get_token"),
    url(r'^api/get_shows', views.get_shows, name="get_shows"),
    url(r'^api/follow', views.follow_show, name="follow_show"),
    url(r'^api/explore', views.explore_client, name="explore_client"),
    url(r'^api/get_suggestions', views.get_suggestions_client,
        name="get_suggestions_client"),
    url(r'^api/mark_as_viewed', views.mark_as_viewed_client,
        name="mark_as_viewed_client"),
    url(r'^api/search_show', views.search_show, name="search_show"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Homepage:
    url(r'^guest_login/', views.guest_login, name="guest_login"),
    url(r'^guest/', views.guest, name="guest"),
    url(r'^$', views.home, name="home"),
)
