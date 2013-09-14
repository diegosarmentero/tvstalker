var current = 0;

$(document).ready(function() {
    $($(".seasons")[current]).attr("style", "display: inline;");
});

function show_season(index) {
    $($(".seasons")[current]).attr("style", "display: none;");
    current = index;
    $($(".seasons")[current]).attr("style", "display: inline;");
}

function previous_season() {
    if(current < $(".seasons").length - 1) {
        $($(".seasons")[current]).attr("style", "display: none;");
        current++;
        $($(".seasons")[current]).attr("style", "display: inline;");
    }
}

function next_season() {
    if(current > 0) {
        $($(".seasons")[current]).attr("style", "display: none;");
        current--;
        $($(".seasons")[current]).attr("style", "display: inline;");
    }
}

function mark_episodes(info) {
    var season = ($(".seasons").length - 1) - current;
    var viewed = $("#check_season" + season).is(":checked");
    for(var i = 1; i < info + 1; i++){
        $("#check_episode" + season + "_" + i).attr("checked", viewed);
    }
}

function mark_as_viewed(showid, season, episode) {
    if(episode == "all") {
        var viewed = $("#check_season" + season).is(":checked");
        $.get("/rpc/mark_as_viewed?showid=" + showid + "&season=" + season +
            "&episode=" + episode + "&viewed=" + viewed, mark_episodes);
    }else{
        var viewed = $("#check_episode" + season + "_" + episode).is(":checked");
        $.get("/rpc/mark_as_viewed?showid=" + showid + "&season=" + season +
            "&episode=" + episode + "&viewed=" + viewed);
    }
}