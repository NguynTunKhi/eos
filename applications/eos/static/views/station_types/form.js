$(document).ready(function() {
    validator = $("form#frmMain").validate({
        rules: {
            station_type: 'required',
            code: 'required',
            qi_type: 'required'
        },
        messages: {
        }
    });
    $('#station_types_code').attr("type", "number");
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
    $("input, textarea, select").formError({remove: true});
    if (!validateMandatory()) return false;
    if (!validateType()) return false;
    if (!validateBussiness()) return false;

    return true;
}

// Validate for fields mandatory
function validateMandatory() {
   if(!validator.form()) return false;
    return true;
}

// Validate for type of fields
function validateType() {
    return true;
}

// Validate for bussiness of fields
function validateBussiness() {
    // Todo
    return true;
}
