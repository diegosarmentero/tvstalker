# -*- coding: utf-8 *-*
#!/usr/bin/env python
#
# Copyright 2011 Chris Baus christopher@baus.net @baus on Twitter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This is a short example program which shows how to use Twitter's
# "Sign In With Twitter" authentication with Google App Engine.
#
#
import functools
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from db.model import StalkerLogin
from gaesessions import get_current_session
from gaesessions import delete_expired_sessions
from auth import twitter
from auth import oauthclient
from auth.keys import TWITTER_CONSUMER_KEY
from auth.keys import TWITTER_CONSUMER_SECRET


TWITTER_REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
TWITTER_ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
TWITTER_AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate"


def authenticated(method):
    """Decorate request handlers with this method to restrict access."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        session = get_current_session()
        twitter_user = session.get("stalker_user")
        if twitter_user is not None:
            self.error(403)
            return

        self.profile = StalkerLogin.get_by_key_name(twitter_user)
        if self.profile is None:
            self.profile = StalkerLogin(key_name=twitter_user,
                login_type='twitter')
            self.profile.save()

        return method(self, *args, **kwargs)
    return wrapper


class SignInWithTwitter(webapp.RequestHandler):
    def get(self):
        key, secret = oauthclient.RetrieveServiceRequestToken(
            TWITTER_REQUEST_TOKEN_URL,
            TWITTER_CONSUMER_KEY,
            TWITTER_CONSUMER_SECRET)
        session = get_current_session()
        if session.is_active():
            session.terminate()
        session['stalker_request_key'] = key
        session['stalker_request_secret'] = secret

        self.redirect(oauthclient.GenerateAuthorizeUrl(
            TWITTER_AUTHENTICATE_URL, key))


class TwitterAuthorized(webapp.RequestHandler):

    def get(self):
        verifier = self.request.get("oauth_verifier")
        session = get_current_session()
        key = session.get('stalker_request_key')
        secret = session.get('stalker_request_secret')

        if key is None or secret is None:
            self.error(500)
            return

        key, secret = oauthclient.ExchangeRequestTokenForAccessToken(
            TWITTER_CONSUMER_KEY,
            TWITTER_CONSUMER_SECRET,
            TWITTER_ACCESS_TOKEN_URL,
            verifier,
            key,
            secret)

        twitapi = twitter.Api(TWITTER_CONSUMER_KEY,
                              TWITTER_CONSUMER_SECRET,
                              key,
                              secret,
                              cache=None)

        twituser = twitapi.VerifyCredentials()
        twitter_user = 'twitter:%s' % twituser.screen_name
        profile = StalkerLogin.get_by_key_name(twitter_user)
        if profile is None:
            profile = StalkerLogin(key_name=twitter_user,
                login_type='twitter')

        profile.access_token_key = key
        profile.access_token_secret = secret
        profile.nick = twituser.screen_name
        profile.save()
        session["stalker_user"] = twitter_user
        self.redirect("/")


class SignOut(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        if session.is_active():
            session.terminate()
        self.redirect("/")


class CleanupSessions(webapp.RequestHandler):
    def get(self):
        while not delete_expired_sessions():
            pass


application = webapp.WSGIApplication([('/oauth/signin_twitter',
                                          SignInWithTwitter),
                                      ('/oauth/twitter', TwitterAuthorized),
                                      ('/oauth/signout', SignOut),
                                      ('/oauth/cleanup_sessions',
                                          CleanupSessions)],
                                         debug=True)


def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
