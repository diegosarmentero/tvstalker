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

function mark_as_viewed(season, episode) {
    alert(season + " - " + episode);
}