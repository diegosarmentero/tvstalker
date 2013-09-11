# -*- coding: utf-8 -*-

from utils import render_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

import shows


@login_required
def home(request):
    """Home Page."""
    shows_filter = ''
    if 'shows' in request.GET:
        shows_filter = request.GET['shows']
        request.session['filter'] = shows_filter
    elif request.session.get('filter', False):
        shows_filter = request.session['filter']
    data = shows.get_shows_per_user(request.user, shows_filter)
    most_rated = shows.get_most_rated_shows(request.user)
    data['recommended'] = most_rated
    return render_response(request, 'index.html', data)


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


@login_required
def genres(request):
    """Genre Page."""
    data = {}
    genre = request.GET.get('genre', '')
    data['genre'] = genre
    if genre:
        results = shows.get_shows_per_genre(genre)
        data['shows'] = results
    data['genres'] = shows.get_genres()
    return render_response(request, 'genres.html', data)


@login_required
def details(request):
    """Details Page."""
    showid = request.GET.get('show', False)
    if not showid:
        return HttpResponseRedirect("/")
    data = shows.get_show_info(showid)
    if 'unfollow' in request.GET:
        showid = request.GET['unfollow']
        shows.unfollow_show(showid, request.user)
    elif 'follow' in request.GET:
        showid = request.GET['follow']
        shows.follow_show(showid, request.user)
    data['following'] = shows.user_is_following(showid, request.user)
    if 'season' in request.GET:
        season = request.GET['season']
        episode = request.GET['episode']
        info = shows.get_episodes_for_season(showid, season, episode)
        data['episode_info'] = info
    else:
        seasons = shows.get_seasons(showid)
        data['seasons'] = seasons
    most_rated = shows.get_most_rated_shows(request.user)
    data['recommended'] = most_rated
    return render_response(request, 'details.html', data)


@login_required
def explore(request):
    """Explore Page."""
    data = {}
    day = request.GET.get('day', '')
    data['day'] = day
    if day:
        results = shows.get_shows_per_day(day)
        data['shows'] = results
    return render_response(request, 'explore.html', data)


def sign_up(request):
    """Sign Up Page."""
    return render_response(request, 'sign-up.html')


@login_required
@require_POST
def rpc(request):
    show_data = shows.get_show(request.POST['search'], request.user)
    data = simplejson.dumps(show_data)

    return HttpResponse(data, mimetype='application/json')


@login_required
def choose_show(request):
    show_data = shows.get_show_by_id(request.GET['showid'], request.user)
    data = simplejson.dumps(show_data)

    return HttpResponse(data, mimetype='application/json')


@login_required
def get_suggestions(request):
    page = int(request.GET.get('page', 0))
    type_ = request.GET.get('type', 'rated')
    response = {}
    if type_ == 'rated':
        results = shows.get_most_rated_shows(request.user, page)
    else:
        results = []

    response['suggestion'] = results
    data = simplejson.dumps(response)

    return HttpResponse(data, mimetype='application/json')