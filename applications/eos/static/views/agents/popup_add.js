/**
 * Created by Admin on 8/2/2017.
 */

$(document).ready(function() {

    $("form#frmPopupAddArea").validate({
        rules: {
            area_code: "required",
        },
        messages: {
            area_code: app.translate('LBL_INPUT_MANDATORY_FIELD'),
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