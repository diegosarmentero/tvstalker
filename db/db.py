# -*- coding: utf-8 -*-

import model


def get_tv_show(title):
    serie = model.Serie.all()
    serie.filter('name =', title)
    if serie.count() == 0:
        return None
    return serie[0]


def check_username_is_valid(self, username):
    account = model.StalkerLogin.all()
    account.filter('login_type = ', 'stalker')
    account.filter('username = ', username)
    if account.count() == 0:
        return (True and username.isalnum())
    return False


def get_activation_account(email, code):
    activate = model.ValidateUser.all()
    activate.filter('validate_code = ', code)
    activate.filter('email = ', email)
    if activate.count() == 0:
        return None
    return activate[0]