$(document).ready(function(){
	$('body').addClass('fixed-sidebar');
	$('.sidebar-collapse').slimScroll({
		height: '100%',
		railOpacity: 0.9
	});

	$('body').on('click', 'a.show_alarm_log_detail', function (e) {
		var id = $(this).attr('data-id');
		var url = $(this).attr('data-url');
        var params = {
            id: id,
        };
        url += '?' + $.param(params);
        if($(".ModalWrap").length == 0){
            $("body").append("<div class='ModalWrap'></div>");
        } else {
            $(".ModalWrap").remove();
            $("body").append("<div class='ModalWrap'></div>");
        }
        $(".ModalWrap").load(url, function (e) {
            var thisInstance = $(this);
            thisInstance.find('.modal').show();
            // Button close
            thisInstance.find(".modal-header span.close, .btnCancel, .btnSave").unbind("click");
            thisInstance.find(".modal-header span.close, .btnCancel").click(function () {
                thisInstance.remove();
            });
        });
    });
});