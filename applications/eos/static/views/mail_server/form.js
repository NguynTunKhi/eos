$(document).ready(function () {
    // See more: https://jqueryvalidation.org/documentation/
    validator = $("form#frmMain").validate({
        rules: {
            mail_server: 'required',
            mail_server_port: {
                required: true,
                digits: true,
            },
            sender_email: 'required',
            sender_email_password: 'required',
        },
        messages: {
            mail_server: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            mail_server_port: {
                required: app.translate('LBL_INPUT_MANDATORY_FIELD'),
                digits: app.translate('LBL_INPUT_DIGIT_VALUE'),
            },
            sender_email: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            sender_email_password: app.translate('LBL_INPUT_MANDATORY_FIELD'),
        },
    });

    $('#btnSave').click(function () {
        if (!validateForm()) return;
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function () {
                $('#frmMain').submit();
            }
        });
    });
});

// Validate form
function validateForm() {
    if (!validateMandatory()) return false;
    return true;
}

// Validate for fields mandatory
function validateMandatory() {
    if(!validator.form()) return false;
    return true;
}

// Validate for bussiness of fields
function validateBussiness() {
}
