# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from db import model
from tvstalker import TvStalkerHandler


class CleanupImages(TvStalkerHandler):

    def get(self):
        images = model.PublishedImages.all()
        for image in images:
            image.delete()


def main():
    application = webapp.WSGIApplication([
        ('/refreshimages', CleanupImages),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
