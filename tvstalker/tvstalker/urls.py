import os

from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from common import views as common_views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Sections
    url(r'^about/', common_views.about, name="about"),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

    # Homepage:
    url(r'^$', common_views.home, name="home"),
)


#if settings.DEBUG:
    #STATIC_DOC_ROOT = os.path.join(os.path.dirname(__file__), "media")

    #static_pattern = patterns('django.views.static',
        #url(r'^media/(?P<path>.*)$', 'serve',
            #{'document_root': STATIC_DOC_ROOT}),
    #)

    #urlpatterns += static_pattern