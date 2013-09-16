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

function get_yesterday() {
    var yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    var dd = yesterday.getDate();
    var mm = yesterday.getMonth() + 1;
    var yyyy = yesterday.getFullYear();
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
        console.log(show.mairdate + ' - ' + today);
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
