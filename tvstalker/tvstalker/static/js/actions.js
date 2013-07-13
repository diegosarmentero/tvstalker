function addTvShow(){
    if($("#search_show").val().length > 0){
        $.pnotify({
            title: 'Show: ' + $("#search_show").val(),
            text: 'Stalking for Tv Show data.\nInformation will be available soon...'
        });
        //$.post("/rpc/", { name: "John", time: "2pm" } );
        $.post("/rpc/", $("#form_search").serializeArray() );
        //server.AddTvShow($("#search_show").val(), updateShows);
        $("#search_show").val("");
    }
}

function updateShows(info){
    if(!info['error']){
        if(info['do_nothing']){
            $.pnotify({
                title: info["title"],
                text: 'Already following!',
                type: 'success'
            });
            return;
        }
        $("#not_following").html("")
        html = "<li class=\"span3\">" +
            "<div class=\"thumbnail border-radius-top\">" +
                "<div class=\"bg-thumbnail-img\">" +
                    "<img class=\"border-radius-top\" src=\"" + info["image_url"] + "\">" +
                "</div>" +
                "<h5><a href=\"/details?show=" + info["name"] + "\">" + info["title"] + "</a></h5>" +
                "<h5><a href=\"/details?show=" + info["name"] + "&episode=" + info["season"] + "x" + info["episode_nro"] + "\">" +
                    "Season: " + info["season"] + "  |  Episode: " + info["episode_nro"] + "</a></h5>" +
            "</div>" +
            "<div class=\"box border-radius-bottom\">" +
                "<p>";
        if(info['today']){
            html += "<span class=\"title_torrent pull-left pull-left\">TODAY</span>";
        }else{
            html += "<span class=\"title_torrent pull-left\">Next Episode</span>" +
                    "<span class=\"number-view pull-right\"> " + info["airdate"] + "</span>";
        }
        html += "</p></div></li>";
        $(html).appendTo("#shows_list");
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