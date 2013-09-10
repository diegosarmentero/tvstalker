TEMPLATE_MULTIPLE = '<li><a onclick="jsfunction" href="javascript:chooseMultiple({0})"><div><img src="{2}" width="150"><b>{1}</b></div></a></li><br>';
// {0} image
// {1} showid
// {2} title
// {3} season_nro
// {4} episode_nro
// {5} next_episode_txt/TODAY
// {6} airdate/empty
TEMPLATE_SHOW = "<li class=\"span3\"><div class=\"thumbnail border-radius-top\"><div class=\"bg-thumbnail-img\"><img class=\"border-radius-top\" src=\"{0}\"></div>" +
                "<h5><a href=\"/details?show={1}\">{2}</a></h5><h5><a href=\"/details?show={1}&season={3}&episode={4}\">" +
                "Season: {3}  |  Episode: {4}</a></h5></div><div class=\"box border-radius-bottom\"><p>" +
                "<span class=\"title_torrent pull-left\">{5}</span><span class=\"number-view pull-right\"> {6}</span></p></div></li>";


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
            //return;
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