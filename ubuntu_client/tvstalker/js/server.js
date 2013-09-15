.pragma library

var URL = "http://tvstalker.tv/";

function login(username, password, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
            callback(result);
        }
    }
    var url = URL + "api/get_token?username=" + username + "&password=" + password;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}

function get_shows(token, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
            callback(result);
        }
    }
    var url = URL + "api/get_shows?token=" + token;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}

function search_show(token, search, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
            callback(result);
        }
    }
    var url = URL + "api/search_show?token=" + token + "&search=" + search;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}

function add_show(token, showid, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
            callback(result);
        }
    }
    var url = URL + "api/follow?token=" + token + "&showid=" + showid;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}

function get_show_details(token, showid, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
            callback(result);
        }
    }
    var url = URL + "api/get_details?token=" + token + "&showid=" + showid;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}

function mark_as_viewed(token, showid, value, season, episode) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
        }
    }
    var url = URL + "api/mark_as_viewed?token=" + token + "&showid=" + showid + "&season=" + season + "&episode=" + episode + "&checked=" + value;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}

function explore_day(day, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
            callback(result);
        }
    }
    var url = URL + "api/explore?day=" + day;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}

function recommend(token, type, page, callback) {
    var doc = new XMLHttpRequest();
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var result = JSON.parse(doc.responseText);
            callback(result);
        }
    }
    var url = URL + "api/get_suggestions?token=" + token + "&page=" + page + "&type=" + type;
    doc.open("get", url);
    doc.setRequestHeader("Content-Encoding", "UTF-8");
    doc.send();
}
