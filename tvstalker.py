# -*- coding: utf-8 *-*
import os
import cgi

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

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


class PyDayHandler(webapp.RequestHandler):

    def user_login(self):
        result = {}
        user = users.get_current_user()
        is_profile = False
        imdb.get_show_info('dexter')
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
            "templates/others/login.html")
        self.response.out.write(template.render(path, data))

    def show_error(self, page_base, message, data):
        data['showerror'] = 'block'
        data['errormessage'] = message
        if 'form' in data:
            data['form'].errors.clear()
        path = os.path.join(os.path.dirname(__file__), page_base)
        self.response.out.write(template.render(path, data))


class NotFoundPageHandler(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/page404.html")
        #result['title'] = 'Error 404'
        #result['message'] = 'La pagina a la que intento acceder no existe.'
        self.response.out.write(template.render(path, {}))


class MainPage(PyDayHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__), "templates/index.html")
        self.response.out.write(template.render(path, result))


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/.*', NotFoundPageHandler),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
