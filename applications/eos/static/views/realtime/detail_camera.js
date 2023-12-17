//$(document).ready(function() {
//    jwplayer.key = '4fIW2J0E542IlbXSI7voFoH2De+H51cCFis9FNAhX2VL+3aa';
//
//    var items = $('.view_camera');
//    var total = items.length;
//    for(var i=0; i<total; i++){
//        var source = $(items[i]).attr('data-source');
//        var img = $(items[i]).attr('data-img');
//        var targetId = $(items[i]).attr('id');
//        // "test" o day la id cua 1 div
//        jwplayer(targetId).setup({
//            // "file": source, // Todo: revert for prod
//            file: source,
//            "image": img,
//            "width": "100%",
//            "aspectratio": "4:3",
//            "autostart": false,
//            "controls": true,
//            "preload": "metadata",
//            "primary": "html5"
//        });
//    }
//});