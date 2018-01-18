
// Generate 32 char random uuid 
function gen_uuid() {
    var uuid = ""
    for (var i=0; i < 32; i++) {
        uuid += Math.floor(Math.random() * 16).toString(16); 
    }
    return uuid
}

//Add upload progress for multipart forms.
$(function() {
    $('#formFileField').submit(function(){
        // Prevent multiple submits
        if ($.data(this, 'submitted')) return false;

        var freq = 1000; // freqency of update in ms
        var uuid = gen_uuid(); // id for this upload so we can fetch progress info.
        var progress_url = '/file/upload_progress/'; // ajax view serving progress info

        // Append X-Progress-ID uuid form action
        this.action += (this.action.indexOf('?') == -1 ? '?' : '&') + 'X-Progress-ID=' + uuid;

        var $progress = $('<div id="upload-progress" class="upload-progress"></div>').
            appendTo(document.body).append('<div class="progress-container"><span class="progress-info">uploading 0%</span><div class="progress-bar"></div></div>');

        // progress bar position
        $progress.css({
            position: 'fixed',
            width: '100%',
            height: '100vh',
            background: '#f7f7f7',
            left: '50%', marginLeft: 0-($progress.width()/2), bottom: '20%'
        }).show();

        // Update progress bar
        function update_progress_info() {
            $progress.show();
            $.getJSON(progress_url, {'X-Progress-ID': uuid}, function(data, status){
                if (data) {
                    var progress = parseInt(data.uploaded) / parseInt(data.length);
                    var width = $progress.find('.progress-container').width()
                    var progress_width = width * progress;
                    $progress.find('.progress-bar').width(progress_width);
                    $progress.find('.progress-info').text('uploading ' + parseInt(progress*100) + '%');
                    console.log(parseInt(progress*100));
                }
                window.setTimeout(update_progress_info, freq);
            });
        };
        window.setTimeout(update_progress_info, freq);

        $.data(this, 'submitted', true); // mark form as submitted.
    });
	
	// Custom input file filed
	(function customInputFile(){
		var inputs = $('.inputfile');
		$(inputs).each(function(){
		  var label  = $(this).next(),
		    labelVal = $(label).html();

		  $(this).on('change', function(e){
		    var fileName = '';
		    if(this.files && this.files.length > 1){
		      fileName = ( $(this).attr('data-multiple-caption') || '' ).replace( '{count}', this.files.length );
		    }
		    else{
		      fileName = e.target.value.split( '\\' ).pop();
		    }

		    if(fileName){
		      $(label).find('span').html(fileName);
		    }
		    else{
		      $(label).html(labelVal);
		    }
		  });
		});
	})();

	// Listen for cloth checkbox form
	(function checkedCloth(){
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
	})();

	// Window resize event
	(function  resizeWindow(){

		$(window).on('resize',function(){
			var winWidth = $(window).width();
			if(winWidth > 623){
				$('.left_sidebar').css('display','block');
				$('#trigger-sidebar').css('display','none');
			}else{
				$('.left_sidebar').css('display','none');
				$('#trigger-sidebar').css('display','block');
			}

		});
	})();

	// Closed status message
	(function closeMsg(){
	var closeIcon = $('.close-btn');
		$(closeIcon).each(function(){
			$(this).click(function(){
				$(this).parent().fadeOut(400);
			});
		});
	})();

	// Trigger sidebar menu
	(function triggerSidebar(){

		$('#trigger-sidebar').click(function(){

			if($('#trigger-sidebar').is(':visible')){
				$('.left_sidebar').toggle('slide',{
					direction: 'left'
				}, 700);
			}else{
				$('.left_sidebar').toggle('slide',{
					direction: 'left'
				}, 700, function(){
					$('#trigger-sidebar').fadeIn();
				});
			}

		});

	})();

});



