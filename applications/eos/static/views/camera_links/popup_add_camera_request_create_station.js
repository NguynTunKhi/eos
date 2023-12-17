/**
 * Created by Admin on 8/2/2017.
 */

$(document).ready(function() {
    app.registerEventsForCommonInput();

    $("form#frmPopupAddCamera").validate({
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
            });
        }
    });
});

function validateBussiness() {
    return true;
}