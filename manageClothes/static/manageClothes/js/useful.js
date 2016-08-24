var USEFUL;
if(!USEFUL){
	USEFUL = {};
};

(function() {
	var func = USEFUL;
	func.decodeURI = function(){
		var a = $('a');
		var i = 0;
		while(a.length){
			var uri = $(a[i]).attr('href');
			$(a[i]).attr('href', decodeURIComponent(uri));
			i++;
		}
	}

	func.accordian = function(target){
		if(! $(target).hasClass('accordian-open')){
			$(target).addClass('accordian-open').slideDown();
		}else{
			$(target).removeClass('accordian-open').slideUp();
		}
	}

})();
