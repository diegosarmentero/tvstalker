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
    url(r'^rpc/choose_show', views.choose_show, name="choose_show"),
    url(r'^rpc/get_suggestions', views.get_suggestions, name="get_suggestions"),
    url(r'^rpc/', views.rpc, name="rpc"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Homepage:
    url(r'^$', views.home, name="home"),
)
