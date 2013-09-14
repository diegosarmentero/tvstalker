$(document).ready(function() {
    var val = getCookie();
    $.get("/rpc/guest_load?following=" + val, loadShows);
})


var CURRENT_SUGGESTION_TYPE = "rated";
var CURRENT_SUGGESTION_PAGE = 0;

TEMPLATE_MULTIPLE = '<li><a onclick="jsfunction" href="javascript:chooseMultiple({0})"><div><img src="{2}" width="150"><b>{1}</b></div></a></li><br>';
// {0} image
// {1} showid
// {2} title
// {3} season_nro
// {4} episode_nro
// {5} next_episode_txt/TODAY
// {6} airdate/empty
TEMPLATE_SHOW = "<li class=\"span3\"><div class=\"thumbnail border-radius-top\"><div class=\"bg-thumbnail-img\"><a onclick=\"jsfunction\" href=\"javascript:notLoggedInMessage()\"><img class=\"border-radius-top\" src=\"{0}\"></a></div>" +
                "<h5><a onclick=\"jsfunction\" href=\"javascript:notLoggedInMessage()\">{2}</a></h5><h5><a onclick=\"jsfunction\" href=\"javascript:notLoggedInMessage()\">" +
                "Season: {3}  |  Episode: {4}</a></h5></div><div class=\"box border-radius-bottom\"><p>" +
                "<span class=\"title_torrent pull-left\">{5}</span><span class=\"number-view pull-right\"> {6}</span></p></div></li>";
// {0} image
// {1} showid
// {2} title
// {3} overview
// {4} next_episode_txt/TODAY
// {5} airdate/empty
TEMPLATE_SUGGESTION = "<li class=\"span5\" id={1}><div class=\"thumbnail border-radius-top\"><div class=\"bg-thumbnail-img\"><a onclick=\"jsfunction\" href=\"javascript:notLoggedInMessage()\">" +
                    "<img class=\"border-radius-top\" width=\"200\" src=\"{0}\"></a></div><div class=\"thumbnail-content-left\">" +
                    "<h4><a onclick=\"jsfunction\" href=\"javascript:notLoggedInMessage()\">{2}</a></h4><h3><a onclick=\"jsfunction\" href=\"javascript:followRecommended({1}, 'rated')\" class=\"btn btn-green-s5\">Follow</a></h3>" +
                    "<br><p>{3}</p></div></div><div class=\"box border-radius-bottom\"><p><span class=\"title_torrent pull-left\">{4}</span>" +
                    "<span class=\"number-view pull-right\">{5}</span></p></div></li>";


String.prototype.format = function() {
    var s = this,
    i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

function addTvShow(){
    if($("#search_show").val().length > 0){
        $.pnotify({
            title: 'Show: ' + $("#search_show").val(),
            text: 'Stalking for Tv Show data.\nInformation will be available soon...'
        });
        var showname = $("#search_show").val();
        var val = getCookie();
        $.get("/rpc/guest?showname=" + showname + "&following=" + val, updateShows);
        $("#search_show").val("");
    }
}

function saveCookie(value) {
    var val = getCookie();
    val += "," + value;
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + 2);
    var c_value = escape(val) + ((2==null) ? "" : "; expires=" + exdate.toUTCString());
    document.cookie= "tvstalker" + "=" + c_value;
}

function getCookie()
{
    var c_value = document.cookie;
    var c_start = c_value.indexOf(" tvstalker=");
    if (c_start == -1){
        c_start = c_value.indexOf("tvstalker=");
    }
    if (c_start == -1){
        c_value = null;
    }else{
        c_start = c_value.indexOf("=", c_start) + 1;
        var c_end = c_value.indexOf(";", c_start);
        if (c_end == -1){
            c_end = c_value.length;
        }
        c_value = unescape(c_value.substring(c_start,c_end));
    }
    return c_value;
}

function chooseMultiple(showid) {
    $.pnotify({
        title: 'Checking selection...',
        text: 'Stalking for Tv Show data.\nInformation will be available soon...'
    });
    var val = getCookie();
    $.get("/rpc/choose_show_guest?showid=" + showid + "&following=" + val, updateShows);
    $('#feature-modal').modal('hide');
}

function loadShows(info) {
    for(var i = 0; i < info.length; i++) {
        updateShows(info[i], true);
    }
}

function updateShows(info){
    if(info["multiple"]) {
        var content = "";
        for(var i=0; i < info["multiple"]; i++){
            content += TEMPLATE_MULTIPLE.format(info["shows"][i][0],
                info["shows"][i][1], info["shows"][i][2]);
        }
        $('#multiple-content').empty();
        $(content).appendTo("#multiple-content");
        $('#feature-modal').modal('toggle');
    } else if(!info['error']){
        if(info['do_nothing']){
            $.pnotify({
                title: info["title"],
                text: 'Already following!',
                type: 'success'
            });
            return;
        }
        $("#not_following").html("")
        var content = TEMPLATE_SHOW.format(info["poster"], info["showid"],
            info["title"], info["season_nro"], info["episode_nro"],
            info["next"], info["airdate"]);
        $(content).appendTo("#shows_list");
        var val = String(getCookie());
        if(val.indexOf(info["showid"]) == -1) {
            saveCookie(info["showid"]);
        }
        $.pnotify({
            title: info["title"],
            text: 'Show info obtained!',
            type: 'success'
        });
    }else{
        $.pnotify({
            title: 'Error!',
            text: info['error'],
            type: 'error'
        });
    }
}

function followRecommended(showid, type) {
    $.pnotify({
        title: 'Adding show...',
        text: 'Stalking for Tv Show data.\nInformation will be available soon...'
    });
    var val = getCookie();
    $.get("/rpc/choose_show_guest?showid=" + showid + "&following=" + val, updateSingleSuggestion);
    $($(".thumbnails-vertical").children("#" + showid)).remove();
}

function updateSuggestions(info) {
    if(info['suggestion'].length > 0) {
        $($(".thumbnails-vertical").children()[0]).remove();
        $($(".thumbnails-vertical").children()[0]).remove();
        addSuggestion(info['suggestion'][0]);
        addSuggestion(info['suggestion'][1]);
    } else {
        if(CURRENT_SUGGESTION_PAGE < 0) {
            CURRENT_SUGGESTION_PAGE++;
        } else {
            CURRENT_SUGGESTION_PAGE--;
        }
    }
}

function updateSingleSuggestion(info) {
    if(!info['suggestion']) {
        updateShows(info);
        $.get("/rpc/get_suggestions?page=0&type=" + CURRENT_SUGGESTION_TYPE, updateSingleSuggestion);
    } else {
        addSuggestion(info['suggestion'][1]);
    }
}

function addSuggestion(info) {
    var content = TEMPLATE_SUGGESTION.format(info["poster"], info["showid"],
        info["title"], info["overview"], info["next"], info["airdate"]);
    $(content).appendTo(".thumbnails-vertical");
}

function getMostRatedSuggestion() {
    CURRENT_SUGGESTION_TYPE = "rated";
    CURRENT_SUGGESTION_PAGE = 0;
    $($(".nav-list").children()[0]).attr("class", "active");
    $($(".nav-list").children()[1]).attr("class", "not-active");
    $.get("/rpc/get_suggestions?page=0&type=rated", updateSuggestions);
}

function getMostViewedSuggestion() {
    CURRENT_SUGGESTION_TYPE = "viewed";
    CURRENT_SUGGESTION_PAGE = 0;
    $($(".nav-list").children()[0]).attr("class", "not-active");
    $($(".nav-list").children()[1]).attr("class", "active");
    $.get("/rpc/get_suggestions?page=0&type=viewed", updateSuggestions);
}

function previous_recommendation() {
    CURRENT_SUGGESTION_PAGE--;
    $.get("/rpc/get_suggestions?page=" + CURRENT_SUGGESTION_PAGE + "&type=" + CURRENT_SUGGESTION_TYPE, updateSuggestions);
}

function next_recommendation() {
    CURRENT_SUGGESTION_PAGE++;
    $.get("/rpc/get_suggestions?page=" + CURRENT_SUGGESTION_PAGE + "&type=" + CURRENT_SUGGESTION_TYPE, updateSuggestions);
}

function notLoggedInMessage() {
    $.pnotify({
        title: 'Not Logged In',
        text: 'You need to create an account to access Calendar information.',
        type: 'info'
    });
}

function removeCookie() {
    document.cookie = 'tvstalker=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    $("#shows_list").html("")
}

function createAccount() {
    var val = getCookie();
    removeCookie();
    window.location.replace("/guest_login/?following=" + val);
}