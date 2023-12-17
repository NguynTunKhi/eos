$(document).ready(function() {
    app.registerEventsForCommonInput();
    $("#btn_Save").click(function() {
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_RECORD_CAMERA'),
            callback: function () {
                $('.btnSave').trigger( "click" );
            }
        });
    });

    $("form#frmPopupRecordCamera").validate({
        rules: {
            camera_source: "required",
            order_no: {digits: true,},
        },
        messages: {
        },
        submitHandler: function (form) {
            if(!validateBussiness()){
                return false;
            }
            app.showConfirmBox({
                content: app.translate('JS_MSG_CONFIRM_SAVE'),
                callback: function () {
                    form.submit();
                }
//                callback: function () {
//                    toastr['success'](app.translate('JS_MSG_SAVE_SUCCESS'));
//                }
            });
        }
    });
});

function validateBussiness() {
    return true;
}