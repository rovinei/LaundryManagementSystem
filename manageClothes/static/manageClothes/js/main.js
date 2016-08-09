function checkedCloth(){
	var clothes = $('.cloth_checkbox');
	var checked_clothes;
	var span_msg = $('#selected_count');
	var btnAction = $('.btn-action');
	var guideMsg = $('#guide-msg');
	$(clothes).change(function(){
		checked_clothes = $('.cloth_checkbox:checked');
		if(checked_clothes.length > 0){
			guideMsg.fadeOut(100);
			btnAction.css('display','inline');
			span_msg.html('<strong>'+checked_clothes.length+'</strong> clothes selected');
		}else{
			span_msg.html('');
			btnAction.fadeOut(100);
			guideMsg.fadeIn(200);
		}
	});
}

function customInputFile(){
	var inputfiles = $('.inputfile');
	$(inputfiles).change(function(){
		if($(this).files.length > 0){
			$(this).next().find('span').html($(this).files.name);
		}

		if($(this).files.length >=2){
			$('#selected_msg').html($(this).files.length+' files selected');
		}
	});
}

function closeMsg(){
	var closeIcon = $('.close-btn');
	$(closeIcon).each(function(){
		$(this).click(function(){
			$(this).parent().fadeOut(400);
		});
	});
}

function triggerSidebar(){
	var sidebar = $('.left_sidebar');

	$('#trigger-sidebar').on('click', function(){
		if(sidebar.css('left') == '-200px'){
			sidebar.animate({
				left:'0px',
			}, 500);
		}else{
			sidebar.animate({
				left:'-200px',
			}, 500);
		}
		
	});

}

function  resizeWindow(){
	var toggleSidebarBtn = $('#trigger-sidebar');
	var sidebar = $('.left_sidebar');
	$(window).resize(function(){
		var winWidth = $(window).width;
		if(winWidth>640){
			sidebar.css('left','0px');
		}

		if(winWidth<640){
			sidebar.css('left','-200px');
		}

	});
}

$(document).ready(function(){
	checkedCloth();
	customInputFile();
	closeMsg();
	triggerSidebar();
	resizeWindow();
});


