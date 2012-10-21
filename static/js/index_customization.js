$("#form_search").live("submit", function(event){
    event.preventDefault();
    addTvShow();
});

$("#btn_search").live("click", function(event){
    event.preventDefault();
    addTvShow();
})