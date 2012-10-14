
(function($){
		
	$(document).ready(function(){

		$('input.box-text').bind('focus blur', function(){
			$(this).toggleClass('focus');
		});

		$('.bg-thumbnail-img').hover(function(){
			$(this).find('.overlay').show();
			$(this).find('.overlay').next().css({'opacity': 0.1});
		},function(){
			$(this).find('.overlay').hide();
			$(this).find('.overlay').next().css({'opacity': 1});
		});

	});


})(jQuery);
