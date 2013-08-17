# -*- coding: utf-8 -*-

from utils import render_response
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

import shows


@login_required
def home(request):
    """Home Page."""
    return render_response(request, 'index.html')


def about(request):
    """About Page."""
    return render_response(request, 'about.html')


def report(request):
    """Report Page."""
    return render_response(request, 'report.html')


@login_required
def profile(request):
    """Profile Page."""
    return render_response(request, 'profile.html')


def sign_up(request):
    """Sign Up Page."""
    return render_response(request, 'sign-up.html')


@require_POST
def rpc(request):
    show_data = shows.get_show(request.POST['search'])
    data = simplejson.dumps(show_data)

    return HttpResponse(data, mimetype='application/json')