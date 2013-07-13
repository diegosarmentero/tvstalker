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
    # RPC
    url(r'^rpc/', views.rpc, name="rpc"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Homepage:
    url(r'^$', views.home, name="home"),
)
