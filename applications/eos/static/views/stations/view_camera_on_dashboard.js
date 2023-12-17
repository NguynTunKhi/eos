$(document).ready(function() {
    jwplayer.key = '4fIW2J0E542IlbXSI7voFoH2De+H51cCFis9FNAhX2VL+3aa';

    $('.vcod').find('.for-camera-action').hide();
    $('.vcod').find('.all-cameras').animate({
        bottom: '+=150'
    }, 300);

    $('body').off('click', '.open_camera');
    $('body').on('click', '.open_camera', function (e) {
        var source = $(this).attr('data-source');
        var img = $(this).attr('data-img');
        var container = $(this).closest('.vcod');
        var camera_links = ['http://27.118.20.209:1935/CAM/CAMTEST6.stream/playlist.m3u8',
            'http://27.118.20.209:1935/CAM/CAMTEST7.stream/playlist.m3u8',
            'http://27.118.20.209:1935/CAM/CAMTEST8.stream/playlist.m3u8'];
        var camera_link = camera_links[parseInt(Math.random() * 3)];
        // "test" o day la id cua 1 div
        jwplayer("test").setup({
            // "file": source, // Todo: revert for prod
            file: source,
            "image": img,
            "width": "100%",
            "aspectratio": "4:3",
            "autostart": true,
            "controls": true,
            "preload": "metadata",
            "primary": "html5"
        });
        container.find('.for-camera').animate({
				right: '0px'
        }, 300, function (e) {
            container.find('.for-camera-action').show();
            container.find('.all-cameras').animate({
                    bottom: '-150px'
            }, 300);
        });
    });

    $('body').off('click', '.action-hide');
    $('body').on('click', '.action-hide', function (e) {
        var thisInstance = this;
        var container = $(this).closest('.vcod');
        if ($(this).hasClass('isOpen')){
            $(this).closest('.for-camera').animate({
                right: '0px'
            }, 300, function () {
                $(thisInstance).removeClass('isOpen');
            });
        } else {
            $(this).closest('.for-camera').animate({
                right: '-250px'
            }, 300, function () {
                $(thisInstance).addClass('isOpen');
            });
        }
    });

    $('body').off('click', '.action-back');
    $('body').on('click', '.action-back', function (e) {
        var container = $(this).closest('.vcod');
        $(this).closest('.for-camera').animate({
				right: '-250px'
        }, 300, function () {
            container.find('.for-camera-action').hide();
            container.find('.all-cameras').animate({
				bottom: '0px'
            }, 300);
        });
    });

    $('body').off('click', '.action-close');
    $('body').on('click', '.action-close', function (e) {
        var container = $(this).closest('.vcod');
        $(this).closest('.for-camera').animate({
				right: '-250px'
        }, 300, function () {
            $(".ModalWrap").remove();
        });
    });

    $('body').off('click', '.all-cameras-close');
    $('body').on('click', '.all-cameras-close', function (e) {
        $(this).closest('.all-cameras').animate({
				bottom: '-150px'
        }, 300, function () {
            $(".ModalWrap").remove();
        });
    });
});