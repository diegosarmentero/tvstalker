
function updateAll(){
    $.post("/rpc/", $("#form_search").serializeArray(), updateShows);
}