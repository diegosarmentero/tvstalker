# -*- coding: utf-8 -*-

from utils import render_response
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """Home Page."""
    return render_response(request, 'index.html')


def login(request):
    """LoginPage."""
    return render_response(request, 'login.html')


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