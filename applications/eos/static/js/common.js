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

function checkEnabled(v) {
    if (v == undefined){
        v = '';
    }
    v = v.toString();
    v = v.toUpperCase();
    if (v == '1' || v == 'TRUE'){
        return true;
    }
    return false;
}

function initPlayVideo(options) {
    jwplayer.key = '4fIW2J0E542IlbXSI7voFoH2De+H51cCFis9FNAhX2VL+3aa';
    var defaults = {
        target: '',
        file: '',
        autostart: true,
    };
    $.extend(defaults, options);
    var items = $(defaults.target);
    for (var i=0; i<items.length; i++) {
        var current_id = $(items[i]).attr('id');
        if (!current_id) {
            continue;
        }
        var current_file = $(items[i]).attr('data-url');
        jwplayer(current_id).setup({
            // "file": "/uploads/example.mp4",
            // file: "http://27.118.20.209:1935/live/CAMTEST2.stream/playlist.m3u8",
            // playlist: [{
            //     sources: [{
            //         file: current_file,
            //         onXhrOpen: function(xhr, url) {
            //             xhr.withCredentials = true;
            //             xhr.setRequestHeader('Access-Control-Request-Headers', 'origin, x-requested-with');
            //             xhr.setRequestHeader('Origin', '*');
            //         }
            //     }]
            // }],
            file: current_file,
            "image": "/uploads/example.jpg",
            "width": "100%",
            "aspectratio": "4:3",
            "autostart": defaults.autostart,
            "controls": true,
            "preload": "metadata",
            "primary": "html5",
        });
    }
}