var server = {};

function InstallFunction(obj, functionName) {
    obj[functionName] = function() { request(functionName, arguments); }
}

//Request class based on the AJAX Google App Engine tutorial
function request(function_name, opt_argv) {
    if (!opt_argv)
        opt_argv = new Array();

    // Find if the last arg is a callback function; save it
    var callback = null;
    var len = opt_argv.length;
    if (len > 0 && typeof opt_argv[len-1] == 'function') {
        callback = opt_argv[len-1];
        opt_argv.length--;
    }
    var async = (callback != null);

    // Build an Array of parameters, w/ function_name being the first parameter
    var params = new Array(function_name);
    for (var i = 0; i < opt_argv.length; i++) {
        params.push(opt_argv[i]);
    }
    var body = JSON.stringify(params);

    var req = new XMLHttpRequest();
    req.open('POST', '/rpc', async);

    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.setRequestHeader("Content-length", body.length);
    req.setRequestHeader("Connection", "close");

    if (async) {
        req.onreadystatechange = function() {
            if(req.readyState == 4 && req.status == 200) {
                var response = null;
                try {
                    response = JSON.parse(req.responseText);
                } catch (e) {
                    response = req.responseText;
                }
                callback(response);
            }
        }
    }

    req.send(body);
}


if( !window.XMLHttpRequest ) XMLHttpRequest = function()
{
  try{ return new ActiveXObject("Msxml2.XMLHTTP.6.0") }catch(e){}
  try{ return new ActiveXObject("Msxml2.XMLHTTP.3.0") }catch(e){}
  try{ return new ActiveXObject("Msxml2.XMLHTTP") }catch(e){}
  try{ return new ActiveXObject("Microsoft.XMLHTTP") }catch(e){}
  throw new Error("Could not find an XMLHttpRequest alternative.")
};

InstallFunction(server, 'AddTvShow');

function addTvShow(){
    if($("#search_show").val().length > 0){
        $.pnotify({
            title: 'Show: ' + $("#search_show").val(),
            text: 'Stalking for Tv Show data.\nInformation will be available soon...'
        });
        server.AddTvShow($("#search_show").val(), updateShows);
        $("#search_show").val("");
    }
}

function updateShows(info){
    if(info){
        $("#not_following").html(info["test"])
        html = "<li class=\"span3\">" +
            "<div class=\"thumbnail border-radius-top\">" +
                "<div class=\"bg-thumbnail-img\">" +
                    "<a class=\"overlay\" href=\"#\">" +
                        "<img src=\"static/img/icons/play.png\">" +
                        "<p>{{ show.episode_title }}</p>" +
                    "</a>" +
                    "<img class=\"border-radius-top\" src=\"{{ show.image }}\">" +
                "</div>" +
                "<h5><a href=\"/details?show={{ show.title }}\">{{ show.title }}</a></h5>" +
                "<h5><a href=\"/details?show={{ show.title }}&episode={{ show.season }}x{{ show.episode }}\">" +
                    "Season: {{ show.season }}  |  Episode: {{ show.episode }}</a></h5>" +
            "</div>" +
            "<div class=\"box border-radius-bottom\">" +
                "<p>" +
                    "{% if today %}" +
                        "<span class=\"title_torrent pull-left pull-left\">TODAY</span>" +
                    "{% else %}" +
                        "<span class=\"title_torrent pull-left\">Next Episode</span>" +
                        "<span class=\"number-view pull-right\"> {{ show.airdate }}</span>" +
                    "{% endif %}" +
                "</p>" +
            "</div>" +
        "</li>";
        $(html).appendTo("#shows_list");
        alert(info);
    }
}