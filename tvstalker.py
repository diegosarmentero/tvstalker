# -*- coding: utf-8 *-*
import os

from google.appengine.api import users
from google.appengine.api import files
from google.appengine.api import images
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from db import db
import imdb


providers = {
    'google': 'www.google.com/accounts/o8/id',
    'yahoo': 'yahoo.com',
    'aol': 'aol.com',
    'openid': 'myopenid.com',
}


def get_twitter_message(message):
    return (u'https://twitter.com/intent/tweet?text=%s' %
        message.replace(' ', '+'))


class TvStalkerHandler(webapp.RequestHandler):

    def user_login(self):
        result = {}
        user = users.get_current_user()
        result['user'] = user
        #is_profile = False
        #imdb.get_show_info('dexter')
        #if user is None:
            #session = get_current_session()
            #twitter_user = session.get("twitter_user")
            #if twitter_user is not None:
                #user = TwitterProfile.get_by_key_name(twitter_user)
                #is_profile = True

        #if user:  # signed in already
            #result['user'] = user
            #if is_profile:
                #result['logout'] = '/oauth/signout'
            #else:
                #result['logout'] = users.create_logout_url(self.request.uri)
            #result['username'] = user.nickname()
        #else:  # let user choose authenticator
            #result['user'] = None
            #result['login'] = '/login'

        return result

    def go_to_login(self, data):
        for name, uri in providers.items():
            data[name] = users.create_login_url(federated_identity=uri)
        path = os.path.join(os.path.dirname(__file__),
            "templates/login.html")
        self.response.out.write(template.render(path, data))


class NotFoundPageHandler(TvStalkerHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),
            "templates/page404.html")
        self.response.out.write(template.render(path, {}))


class MainPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        if result['user'] is None:
            self.go_to_login(result)
        else:
            path = os.path.join(os.path.dirname(__file__),
                "templates/index.html")
            serie = db.get_tv_show('dexter')
            #url = images.get_serving_url(files.blobstore.get_blob_key(
                #serie.image_name))
            #result['image_key'] = url
            self.response.out.write(template.render(path, result))


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/.*', NotFoundPageHandler),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
