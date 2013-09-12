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
TEMPLATE_SHOW = "<li class=\"span3\"><div class=\"thumbnail border-radius-top\"><div class=\"bg-thumbnail-img\"><a href='/details?show={1}'><img class=\"border-radius-top\" src=\"{0}\"></a></div>" +
                "<h5><a href=\"/details?show={1}\">{2}</a></h5><h5><a href=\"/details?show={1}&season={3}&episode={4}\">" +
                "Season: {3}  |  Episode: {4}</a></h5></div><div class=\"box border-radius-bottom\"><p>" +
                "<span class=\"title_torrent pull-left\">{5}</span><span class=\"number-view pull-right\"> {6}</span></p></div></li>";
// {0} image
// {1} showid
// {2} title
// {3} overview
// {4} next_episode_txt/TODAY
// {5} airdate/empty
TEMPLATE_SUGGESTION = "<li class=\"span5\" id={1}><div class=\"thumbnail border-radius-top\"><div class=\"bg-thumbnail-img\"><a href=\"/details?show={1}\">" +
                    "<img class=\"border-radius-top\" width=\"200\" src=\"{0}\"></a></div><div class=\"thumbnail-content-left\">" +
                    "<h4><a href=\"/details?show={1}\">{2}</a></h4><h3><a onclick=\"jsfunction\" href=\"javascript:followRecommended({1}, 'rated')\" class=\"btn btn-green-s5\">Follow</a></h3>" +
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
    //alert("bla bla {0} asdasd {1}".format("diego", "gatox"));
    if($("#search_show").val().length > 0){
        $.pnotify({
            title: 'Show: ' + $("#search_show").val(),
            text: 'Stalking for Tv Show data.\nInformation will be available soon...'
        });
        $.post("/rpc/", $("#form_search").serializeArray(), updateShows);
        $("#search_show").val("");
    }
}

function chooseMultiple(showid) {
    $.pnotify({
        title: 'Checking selection...',
        text: 'Stalking for Tv Show data.\nInformation will be available soon...'
    });
    $.get("/rpc/choose_show?showid=" + showid, updateShows);
    $('#feature-modal').modal('hide');
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
    $.get("/rpc/choose_show?showid=" + showid, updateSingleSuggestion);
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
    $($(".nav-list").children()[0]).attr("class", "active");
    $($(".nav-list").children()[1]).attr("class", "not-active");
    $.get("/rpc/get_suggestions?page=0&type=rated", updateSuggestions);
}

function getMostViewedSuggestion() {
    CURRENT_SUGGESTION_TYPE = "viewed";
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