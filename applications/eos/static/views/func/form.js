$(document).ready(function() {
    // See more: https://jqueryvalidation.org/documentation/
    validator = $("form#frmMain").validate({
        rules: {
            func_code: {
                required: true,
                maxlength: 64,
            },
            func_name: {
                required: true,
                maxlength: 128,
            },
        },
    });
    
    $('#btnSave').click(function() {
        if (!validateForm()) return;
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function() {
                $('#frmMain').submit();
            }
        });
    });
});

// Validate form
function validateForm() {
    if (!validateMandatory()) return false;
    if (!validateBussiness()) return false;

    return true;
}

// Validate for fields mandatory
function validateMandatory() {
    if(!validator.form()) return false;
    return true;
}

// Validate for bussiness of fields
function validateBussiness() {
    // Todo
    return true;
}
