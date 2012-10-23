# -*- coding: utf-8 *-*
import os
import cgi
import datetime
import hashlib
import uuid

from google.appengine.api import users
from google.appengine.api import files
from google.appengine.api import images
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from gaesessions import get_current_session

from db import (
    db,
    model,
)


providers = {
    'google': 'www.google.com/accounts/o8/id',
}


def get_twitter_message(message):
    return (u'https://twitter.com/intent/tweet?text=%s' %
        message.replace(' ', '+'))


class InvalidUsername(Exception):
    """Invalid Password Exception."""


class InvalidPassword(Exception):
    """Invalid Password Exception."""


class DisplayShow(object):

    def __init__(self, show, episode):
        self.name = show.name
        self.title = show.title
        url = images.get_serving_url(files.blobstore.get_blob_key(
            show.image_name))
        self.image = url
        self.season = show.last_season
        if episode is not None:
            self.episode_title = episode.title
            self.episode = episode.nro
            if episode.airdate == datetime.date.today():
                self.today = True
            else:
                self.today = False
                date = "%s %i, %i" % (
                    episode.airdate.strftime('%B')[:3],
                    episode.airdate.day, episode.airdate.year)
                self.airdate = date
        else:
            self.episode_title = 'N/A'
            self.episode = 'N/A'
            self.today = False
            self.airdate = 'N/A'


class TvStalkerHandler(webapp.RequestHandler):

    def user_login(self):
        result = {}
        user = users.get_current_user()
        if user is not None:
            key_name = 'google:%s' % user.nickname()
            login = model.StalkerLogin.get_by_key_name(key_name)
            if login is None:
                login = model.StalkerLogin(key_name=key_name,
                    user=user, login_type='google')
                login.username = user.nickname()
            login.put()
            if login.login_type == 'stalker':
                result['is_stalker_user'] = True
            result['logout'] = users.create_logout_url(self.request.uri)
        else:
            session = get_current_session()
            stalker_user = session.get("stalker_user")
            password = session.get("stalker_request_key")
            if stalker_user is not None:
                login = model.StalkerLogin.get_by_key_name(stalker_user)
                if login and login.access_token_key != password:
                    login = None
            else:
                login = None
            result['logout'] = '/oauth/signout'
        result['user'] = login

        return result

    def go_to_login(self, error=False):
        url = '/login'
        if error:
            url += '?error=true'
        self.redirect(url)

    def go_to_home(self, data):
        following = db.get_user_shows(data['user'])
        shows = []
        for follow in following:
            episode = db.obtain_most_recent_episode(follow.serie)
            display = DisplayShow(follow.serie, episode)
            if data['filter'] != 'today' or (
               data['filter'] == 'today' and display.today):
                shows.append(display)
        data['shows'] = shows
        path = os.path.join(os.path.dirname(__file__),
            "templates/index.html")
        self.response.out.write(template.render(path, data))


class NotFoundPageHandler(TvStalkerHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),
            "templates/page404.html")
        self.response.out.write(template.render(path, {}))


class ProfilePage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        message = cgi.escape(self.request.get('message'))
        error = cgi.escape(self.request.get('error'))
        if error:
            result['error'] = error
        else:
            result['message'] = message
        profile = db.get_profile(result['user'])
        if profile is not None:
            result['profile'] = profile
            if profile.avatar:
                url = images.get_serving_url(files.blobstore.get_blob_key(
                    profile.avatar))
                result['image_url'] = url
        if result['user'] is None:
            self.go_to_login()
        else:
            path = os.path.join(os.path.dirname(__file__),
                "templates/profile.html")
            self.response.out.write(template.render(path, result))

    def post(self):
        result = self.user_login()
        try:
            login = result['user']
            username = cgi.escape(self.request.get('username'))
            name = cgi.escape(self.request.get('name'))
            lastname = cgi.escape(self.request.get('lastname'))
            #image = self.request.get('image')
            email = cgi.escape(self.request.get('email'))
            password = cgi.escape(self.request.get('password'))
            confirm = cgi.escape(self.request.get('confirm'))
            # Check that the proper fields are valid (password and confirm)
            if username != login.username:
                valid = db.check_username_is_valid(username)
                if not valid:
                    raise InvalidUsername()
            if password != confirm:
                raise Exception("Invalid Password")
            profile = db.get_profile(result['user'])
            if profile is None:
                profile = model.User()
            # Search for login and update username
            # Update password in login
            password = hashlib.sha512(password).hexdigest()
            login.username = username
            if login.login_type == 'stalker':
                login.access_token_key = password
            login.put()
            profile.login = login
            profile.name = name
            profile.lastname = lastname
            profile.email = email
            # Save Avatar
            #file_name = files.blobstore.create(
                #mime_type='application/octet-stream')
            #with files.open(file_name, 'a') as f:
                #f.write(str(image))
            #files.finalize(file_name)
            #profile.avatar = file_name
            profile.put()
            # Update Session
            stalker_user = 'stalker:%s' % username
            session = get_current_session()
            session["stalker_user"] = stalker_user
            session["stalker_request_key"] = password
        except InvalidUsername:
            self.redirect('/profile?error=%s' %
                "Invalid Username or already taken")
        except InvalidPassword:
            self.redirect('/profile?error=%s' % "Password don't match'")
        #except Exception, reason:
            #self.redirect('/profile?error=%s' % str(reason))
        else:
            self.redirect('/profile?message=%s' % "Profile Updated!")


class SettingsPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        if result['user'] is None:
            self.go_to_login()
        else:
            path = os.path.join(os.path.dirname(__file__),
                "templates/setting.html")
            self.response.out.write(template.render(path, result))


class ValidatePage(TvStalkerHandler):
    def get(self):
        email = cgi.escape(self.request.get('email'))
        path = os.path.join(os.path.dirname(__file__),
            "templates/validate.html")
        data = {'email': email}
        error = cgi.escape(self.request.get('error'))
        if error:
            data['error'] = True
        self.response.out.write(template.render(path, data))

    def post(self):
        email = cgi.escape(self.request.get('email'))
        code = cgi.escape(self.request.get('code'))
        validate = db.get_activation_account(email, code)
        if validate is not None:
            key_name = 'stalker:%s' % validate.username
            login = model.StalkerLogin(key_name=key_name, login_type='stalker')
            login.access_token_key = validate.password
            login.username = validate.username
            login.put()
            user = model.User()
            user.email = email
            user.password = validate.password
            user.login = login
            user.put()
            validate.delete()
            self.go_to_login()
        else:
            # Activation not founnd
            self.redirect('/validate?error=true&email=%s' % email)


class SignUpPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        error = cgi.escape(self.request.get('error'))
        if error:
            result['error'] = True
        if result['user'] is not None:
            self.go_to_home(result)
        else:
            path = os.path.join(os.path.dirname(__file__),
                "templates/sign-up.html")
            self.response.out.write(template.render(path, result))

    def post(self):
        email = cgi.escape(self.request.get('email'))
        username = cgi.escape(self.request.get('username'))
        password = cgi.escape(self.request.get('password'))
        password = hashlib.sha512(password).hexdigest()
        valid = db.check_username_is_valid(username)
        if valid:
            db.clean_previous_activation(email)
            validate = model.ValidateUser()
            validate.username = username
            validate.email = email
            validate.password = password
            validate.validate_code = str(uuid.uuid4())
            validate.put()
            self.send_validate_email(email, validate.validate_code)
            self.redirect('/validate?email=%s' % email)
        else:
            # Invalid username or already taken
            self.redirect('/SignUp?error=true')

    def send_validate_email(self, email, code):
        mailFrom = "notifications@tvstalker.tv"
        subject = "Activate Account"
        body = "This is your activation code: %s" % code
        mail.send_mail(mailFrom, email, subject, body)


class LoginPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        error = cgi.escape(self.request.get('error'))
        if error:
            result['error'] = True
        for name, uri in providers.items():
            result[name] = users.create_login_url(federated_identity=uri)
        path = os.path.join(os.path.dirname(__file__),
            "templates/login.html")
        self.response.out.write(template.render(path, result))

    def post(self):
        username = cgi.escape(self.request.get('username'))
        password = cgi.escape(self.request.get('password'))
        password = hashlib.sha512(password).hexdigest()
        stalker_user = 'stalker:%s' % username
        login = model.StalkerLogin.get_by_key_name(stalker_user)
        if login is None or login.access_token_key != password:
            # Invalid login
            self.go_to_login(True)
            return
        # Load session
        session = get_current_session()
        session["stalker_user"] = stalker_user
        session["stalker_request_key"] = password
        self.redirect('/')


class AboutPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/about.html")
        self.response.out.write(template.render(path, result))


class UnfollowPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        show_name = cgi.escape(self.request.get('show'))
        if result['user'] is None:
            self.go_to_login()
        else:
            show = db.get_tv_show(show_name)
            following = db.is_already_following(result['user'], show)
            following.delete()
            self.redirect('/')


class DetailsPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        show_name = cgi.escape(self.request.get('show'))
        episode = cgi.escape(self.request.get('episode'))
        if result['user'] is None:
            self.go_to_login()
        else:
            show = db.get_tv_show(show_name)
            result['show'] = show
            url = images.get_serving_url(files.blobstore.get_blob_key(
                show.image_name))
            result['image_url'] = url
            # Get episodes
            season = db.get_last_season(show)
            # Check if it is detail or episode info
            if episode:
                nro = episode.split('x')[1]
                if nro.isdigit():
                    nro = int(nro)
                else:
                    nro = 1
                episode_info = db.get_episodes_for_season_and_nro(season, nro)
                result['episode_info'] = episode_info
            else:
                episodes = db.get_episodes_for_season(season)
                result['episodes'] = episodes
            path = os.path.join(os.path.dirname(__file__),
                "templates/details.html")
            self.response.out.write(template.render(path, result))


class MainPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        filter_option = cgi.escape(self.request.get('shows'))
        result['filter'] = filter_option
        if result['user'] is None:
            self.go_to_login()
        else:
            self.go_to_home(result)


class ReportPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        if result['user'] is None:
            self.go_to_login()
        else:
            path = os.path.join(os.path.dirname(__file__),
                "templates/report.html")
            self.response.out.write(template.render(path, result))

    def post(self):
        result = self.user_login()
        if result['user'] is None:
            self.go_to_login()
        else:
            bug = cgi.escape(self.request.get('bug'))
            self.notify_bug(bug, result['user'])
            self.redirect('/')

    def notify_bug(self, message, user):
        mailFrom = "notifications@tvstalker.tv"
        body = "From: %s\n%s" % (user.username, message)
        mail.send_mail(mailFrom, "diegosarmentero@tvstalker.tv",
            "Tv Stalker Bug", body)


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/SignUp', SignUpPage),
        ('/profile', ProfilePage),
        ('/settings', SettingsPage),
        ('/login', LoginPage),
        ('/validate', ValidatePage),
        ('/about', AboutPage),
        ('/details', DetailsPage),
        ('/unfollow', UnfollowPage),
        ('/report', ReportPage),
        ('/.*', NotFoundPageHandler),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
