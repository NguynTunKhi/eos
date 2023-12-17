
$(document).ready(function() {
    app.registerEventsForCommonInput();

    $('.chosen-container-single').css('width', '100%');
    
    $("form#frmPopupUpdateAlarmLogs").validate({
        rules: {
            status: "required",
        },
        messages: {
            status: app.translate('LBL_INPUT_MANDATORY_FIELD'),
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