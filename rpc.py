# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson

from rpc_methods import RPCMethods
from tvstalker import TvStalkerHandler


class RPCHandler(TvStalkerHandler):

    def __init__(self):
        super(RPCHandler, self).__init__()
        self.methods = RPCMethods()

    def get(self):
        user_data = self.user_login()
        if user_data['user'] is None:
            return
        func = None

        action = self.request.get('action')
        if action:
            if action[0] == '_':
                self.error(403)  # access denied
                return
            else:
                func = getattr(self.methods, action, None)

        if not func:
            self.error(404)  # file not found
            return

        args = ()
        while True:
            key = 'arg%d' % len(args)
            val = self.request.get(key)
            if val:
                args += (simplejson.loads(val),)
            else:
                break
        result = func(*args, **user_data)
        self.response.out.write(simplejson.dumps(result))

    def post(self):
        user_data = self.user_login()
        if user_data['user'] is None:
            return
        args = simplejson.loads(self.request.body)
        func, args = args[0], args[1:]

        if func[0] == '_':
            self.error(403)  # access denied
            return

        func = getattr(self.methods, func, None)
        if not func:
            self.error(404)  # file not found
            return

        result = func(*args, **user_data)
        self.response.out.write(simplejson.dumps(result))


def main():
    application = webapp.WSGIApplication([
        ('/rpc', RPCHandler),
        ], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
