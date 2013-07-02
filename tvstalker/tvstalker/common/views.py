# -*- coding: utf-8 -*-

from utils import render_response


def home(request):
    """ Intro/Splash screen.
    """
    return render_response(request, 'index.html')