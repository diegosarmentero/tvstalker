# -*- coding: utf-8 *-*
import os
import cgi
import hashlib
import uuid

from google.appengine.api import users
#from google.appengine.api import files
#from google.appengine.api import images
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
            result['logout'] = users.create_logout_url(self.request.uri)
        else:
            session = get_current_session()
            stalker_user = session.get("stalker_user")
            if stalker_user is not None:
                login = model.StalkerLogin.get_by_key_name(stalker_user)
            else:
                login = None
            result['logout'] = '/oauth/signout'
        result['user'] = login

        return result

    def go_to_login(self, data, error=False):
        url = '/login'
        if error:
            url += '?error=true'
        self.redirect(url)

    def go_to_home(self, data):
        #url = images.get_serving_url(files.blobstore.get_blob_key(
            #serie.image_name))
        #result['image_key'] = url
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
        if result['user'] is None:
            self.go_to_login(result)
        else:
            path = os.path.join(os.path.dirname(__file__),
                "templates/profile.html")
            self.response.out.write(template.render(path, result))


class SettingsPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        if result['user'] is None:
            self.go_to_login(result)
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
            self.go_to_login({}, True)
            return
        # Load session
        session = get_current_session()
        session["stalker_user"] = stalker_user
        self.go_to_home()


class AboutPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        path = os.path.join(os.path.dirname(__file__),
            "templates/about.html")
        self.response.out.write(template.render(path, result))


class MainPage(TvStalkerHandler):
    def get(self):
        result = self.user_login()
        if result['user'] is None:
            self.go_to_login(result)
        else:
            self.go_to_home(result)


def main():
    application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/SignUp', SignUpPage),
        ('/profile', ProfilePage),
        ('/settings', SettingsPage),
        ('/login', LoginPage),
        ('/validate', ValidatePage),
        ('/about', AboutPage),
        ('/.*', NotFoundPageHandler),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
