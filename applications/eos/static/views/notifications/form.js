
$(document).ready(function() {
    $('#btnDelete1, #btnDelete2').click(function() {
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_DELETE'),
            callback: function() {
                var data = {
                    notification_id: $('#notification_id').val(),
                };
                var url = $('#btnDelete1').data('url');
                app.postAjax({
                    url: url,
                    data: data,
                    callback: function (res) {
                        if (res.success) {
                            window.location.href = "/eos/notifications/index";
                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });
    
    
});

