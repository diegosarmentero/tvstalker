from gaesessions import SessionMiddleware


def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app,
        cookie_key=("tv_stalker tv_stalker tv_stalker tv_stalker "
                    "tv_stalker tv_stalker tv_stalker"),
        cookie_only_threshold=0)
    return app
