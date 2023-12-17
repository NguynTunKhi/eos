
$(document).ready(function() {
    $('body').off('click', '.product-box');
    $('body').on('click', '.product-box', function (e) {
        if (e.target.className.indexOf('add-alert') == -1) {
            // Redirect to station page
            var station_type = $(this).attr('data-st');
            var params = {
                station_type: station_type
            };
            var url = $(this).attr('data-redirect');
            window.location.href = url + '?' + $.param(params);
            e.preventDefault();
            return;
        }
        // Show popup in order to add new alert
        var url = $(this).attr('data-url');
        var station_type = $(e.target).attr('data-st');
        var station_id = $(e.target).attr('data-station_id');
        var indicator_id = $(e.target).attr('data-indicator_id');
        var params = {
            station_type: station_type,
            station_id: station_id,
            indicator_id: indicator_id,
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
            // Button save
            thisInstance.find(".btnSave").click(function () {
                if($(this).closest(".modal").find("form").validate().form() == false){
                    return;
                }
                var currentForm = $(this).closest(".modal").find("form");
                var url2 = currentForm.attr('action');
                $.ajax({
                    type: "POST",
                    dataType: 'json',
                    url: url2,
                    data: currentForm.serialize(),
                    success: function(data){
                        if(data.success){
                            // Remove wrap tag
                            thisInstance.remove();
                            toastr['success'](app.translate('JS_MSG_SAVE_SUCCESS'));
                        } else {
                            thisInstance.find(".errors").html(data.message);
                        }
                    },
                    error: function(err){
                        thisInstance.find(".errors").html(err.status + ": " + err.statusText);
                    }
                 });
            });
        });
    });

    $('body').off('click', '.view-camera');
    $('body').on('click', '.view-camera', function (e) {
        var station_id = $(this).attr('data-st');
        var url = $(this).attr('data-url');
        url += '?' + $.param({station_id: station_id});
        if($(".ModalWrap").length == 0){
            $("body").append("<div class='ModalWrap'></div>");
        } else {
            $(".ModalWrap").remove();
            $("body").append("<div class='ModalWrap'></div>");
        }
        $(".ModalWrap").load(url, function (e) {
            var thisInstance = $(this);
        });
    });
});