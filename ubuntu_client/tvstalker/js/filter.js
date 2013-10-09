function get_today() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
    if(dd < 10){
        dd = "0" + dd;
    }
    if(mm < 10){
        mm = "0" + mm;
    }

    return yyyy + "-" + mm + "-" + dd;
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

function filter_by_date(date) {
    for(var i = 0; i < showsModel.count; i++) {
        var show = showsModel.get(i);
        if(show.mdayOfWeek == date){
            show.mvisible = true;
        }else{
            show.mvisible = false;
        }
    }
}
