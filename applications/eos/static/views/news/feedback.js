$(document).ready(function() {
    // See more: https://jqueryvalidation.org/documentation/
    validator = $("form#frmMain").validate({
        rules: {
            summary: 'required',
        }
    });
    
    $('#btnSave').click(function() {
        $('#province_name').val($('#news_province_id option:selected').text())
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
