# -*- coding: utf-8 -*-

from utils import render_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

import shows


@login_required
def home(request):
    """Home Page."""
    if request.session.get('new_user', False):
        shows_info = request.session["from_guest"]
        for val in shows_info:
            if val.isdigit():
                shows.get_show_by_id(val, request.user)
    shows_filter = ''
    if 'shows' in request.GET:
        shows_filter = request.GET['shows']
        request.session['filter'] = shows_filter
    elif request.session.get('filter', False):
        shows_filter = request.session['filter']
    else:
        shows_filter = 'all'
    data = shows.get_shows_per_user(request.user, shows_filter)
    most_rated = shows.get_most_rated_shows(request.user)
    data['recommended'] = most_rated
    data['filter'] = shows_filter
    return render_response(request, 'index.html', data)


@staff_member_required
def update(request):
    """Update Page."""
    data = shows.get_shows_to_update()
    return render_response(request, 'update.html', data)


def guest(request):
    """Guest Page."""
    shows_filter = ''
    if 'shows' in request.GET:
        shows_filter = request.GET['shows']
        request.session['filter'] = shows_filter
    elif request.session.get('filter', False):
        shows_filter = request.session['filter']
    else:
        shows_filter = 'all'
    data = {}
    most_rated = shows.get_most_rated_shows()
    data['recommended'] = most_rated
    data['filter'] = shows_filter
    return render_response(request, 'guest/guest.html', data)


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
    if not showid or not showid.isdigit():
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
        if not season.isdigit() or not episode.isdigit():
            season = 1
            episode = 1
        info = shows.get_episodes_for_season(showid, season, episode)
        data['episode_info'] = info
    else:
        seasons = shows.get_seasons(showid, request.user)
        data['seasons'] = seasons
    most_rated = shows.get_most_rated_shows(request.user)
    data['recommended'] = most_rated
    return render_response(request, 'details.html', data)


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


def rpc_guest(request):
    following = request.GET['following'].split(",")
    show_data = shows.get_show(request.GET['showname'], None)
    if "showid" in show_data and str(show_data["showid"]) in following:
        show_data = {"do_nothing": True}
    data = simplejson.dumps(show_data)

    return HttpResponse(data, mimetype='application/json')


def rpc_guest_load(request):
    following = request.GET['following'].split(",")
    shows_info = []
    for val in following:
        if val.isdigit():
            show_data = shows.get_show_by_id(val, None)
            shows_info.append(show_data)

    data = simplejson.dumps(shows_info)

    return HttpResponse(data, mimetype='application/json')


@login_required
def choose_show(request):
    show_data = shows.get_show_by_id(request.GET['showid'], request.user)
    data = simplejson.dumps(show_data)

    return HttpResponse(data, mimetype='application/json')


def choose_show_guest(request):
    following = request.GET['following'].split(",")
    show_data = shows.get_show_by_id(request.GET['showid'], None)
    if "showid" in show_data and str(show_data["showid"]) in following:
        show_data = {"do_nothing": True}
    data = simplejson.dumps(show_data)

    return HttpResponse(data, mimetype='application/json')


def get_suggestions(request):
    page = int(request.GET.get('page', 0))
    type_ = request.GET.get('type', 'rated')
    response = {}
    if request.user.is_anonymous():
        user = None
    else:
        user = request.user
    if type_ == 'rated':
        results = shows.get_most_rated_shows(user, page)
    else:
        results = shows.get_most_viewed_shows(user, page)

    response['suggestion'] = results
    data = simplejson.dumps(response)

    return HttpResponse(data, mimetype='application/json')


def guest_login(request):
    following = request.GET.get('following', "").split(",")
    request.session['from_guest'] = following
    request.session['new_user'] = True

    return render_response(request, 'guest/guest_login.html')


@login_required
def mark_as_viewed(request):
    result = True
    if ("showid" in request.GET and "season" in request.GET and
        "episode" in request.GET):
        showid = request.GET['showid']
        season = request.GET['season']
        episode = request.GET['episode']
        viewed = request.GET['viewed'] == "true"
        if showid.isdigit() and season.isdigit():
            result = shows.mark_as_viewed(request.user, int(showid),
                int(season), episode, viewed)

    data = simplejson.dumps([result])
    return HttpResponse(data, mimetype='application/json')


# Client API
def _validate_token(request):
    user = None
    token = request.GET.get('token', '')
    tokendb = shows.models.UserToken.objects.filter(
        token=token)
    if len(tokendb) == 1:
        user = tokendb[0].user

    return user


def get_token(request):
    response = {}
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    users = shows.models.User.objects.filter(username=username)
    if len(users) == 1 and users[0].check_password(password):
        user = users[0]
        tokendb, create = shows.models.UserToken.objects.get_or_create(
            user=user)
        tokendb.create_token()
        tokendb.save()
        response['token'] = tokendb.token
    else:
        response['invalid'] = 'Invalid User'

    data = simplejson.dumps(response)
    return HttpResponse(data, mimetype='application/json')


def get_shows(request):
    response = []
    user = _validate_token(request)
    if user:
        response = shows.get_shows_per_user_client(user)

    data = simplejson.dumps(response)
    return HttpResponse(data, mimetype='application/json')


def search_show(request):
    show_data = None
    user = _validate_token(request)
    if user:
        search = request.GET.get('search', '')
        show_data = shows.get_show(search, user, client=True)

    data = simplejson.dumps(show_data)
    return HttpResponse(data, mimetype='application/json')


def get_details(request):
    data = {}
    user = _validate_token(request)
    if user:
        showid = request.GET.get('showid', '')
        data = shows.get_show_info(showid, client=True)
        data['following'] = shows.user_is_following(showid, user)
        seasons = shows.get_seasons_client(showid, user)
        data['seasons'] = seasons

    data = simplejson.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def mark_as_viewed_client(request):
    result = True
    user = _validate_token(request)
    if user:
        showid = request.GET.get('showid', '')
        season = request.GET.get('season', '')
        episode = request.GET.get('episode', '')
        checked = request.GET.get('checked', '')
        result = shows.mark_as_viewed(user, int(showid),
            int(season), int(episode), checked)

    data = simplejson.dumps([result])
    return HttpResponse(data, mimetype='application/json')


def explore_client(request):
    day = request.GET.get('day', '')
    results = shows.get_shows_per_day(day)

    data = simplejson.dumps(results)
    return HttpResponse(data, mimetype='application/json')


def get_suggestions_client(request):
    page = int(request.GET.get('page', 0))
    type_ = request.GET.get('type', 'rated')
    user = _validate_token(request)
    results = []
    if user:
        if type_ == 'rated':
            results = shows.get_most_rated_shows(user, page, 6)
        else:
            results = shows.get_most_viewed_shows(user, page, 6)

    data = simplejson.dumps(results)
    return HttpResponse(data, mimetype='application/json')


def follow_show(request):
    show_data = None
    user = _validate_token(request)
    if user:
        showid = int(request.GET.get('showid', 0))
        show_data = shows.get_show_by_id(showid, user, client=True)
        shows.follow_show(showid, user)

    data = simplejson.dumps(show_data)
    return HttpResponse(data, mimetype='application/json')


#@staff_member_required
#def update_shows(request):
    #data = simplejson.dumps([True])
    #return HttpResponse(data, mimetype='application/json')