function get_today() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth();
    var yyyy = today.getFullYear();

    return yyyy + "-" + mm + "-" + dd;
}

function get_yesterday() {

}

function filter_all() {
    for(var i = 0; i < showsModel.count; i++) {
        var show = showsModel.get(i);
        show.mvisible = true;
    }
}

function filter_current() {
    for(var i = 0; i < showsModel.count; i++) {
        var show = showsModel.get(i);
        show.mvisible = show.mcurrent;
    }
}

function filter_today() {
    var today = get_today();
    for(var i = 0; i < showsModel.count; i++) {
        var show = showsModel.get(i);
        if(show.mairdate == today){
            show.mvisible = true;
        } else {
            show.mvisible = false;
        }
    }
}

function filter_yesterday() {
    var yesterday = get_yesterday();
    for(var i = 0; i < showsModel.count; i++) {
        var show = showsModel.get(i);
        if(show.mairdate == yesterday){
            show.mvisible = true;
        } else {
            show.mvisible = false;
        }
    }
}

function filter_by_date(date) {
    console.log(date);
    for(var i = 0; i < showsModel.count; i++) {
        var show = showsModel.get(i);
        console.log(show.mdayOfWeek);
        if(show.mdayOfWeek == date){
            show.mvisible = true;
        }else{
            show.mvisible = false;
        }
    }
}
