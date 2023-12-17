$(document).ready(function() {
    validator = $("form#frmMain").validate({
    rules: {
        indicator: 'required',
        indicator_type: 'required',
        source_name: 'required',
        tendency_value: {
                required: true,
                number: true,
            },
        preparing_value: {
                required: true,
                number: true,
            },
        exceed_value: {
                required: true,
                number: true,
            },
    },
    messages: {
        indicator: app.translate('LBL_INPUT_MANDATORY_FIELD'),
        indicator_type: app.translate('LBL_INPUT_MANDATORY_FIELD'),
        source_name: app.translate('LBL_INPUT_MANDATORY_FIELD'), 
        tendency_value : {
                required : app.translate('LBL_INPUT_MANDATORY_FIELD'),
                number : app.translate('LBL_INPUT_INTEGER'),
            }, 
        preparing_value : {
                required : app.translate('LBL_INPUT_MANDATORY_FIELD'),
                number : app.translate('LBL_INPUT_INTEGER'),
            }, 
        exceed_value : {
                required : app.translate('LBL_INPUT_MANDATORY_FIELD'),
                number : app.translate('LBL_INPUT_INTEGER'),
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
    $('#indicators_exceed_value').change(function() {
      $('#indicators_preparing_value').val($('#indicators_exceed_value').val()*7/10);
      $('#indicators_tendency_value').val($('#indicators_exceed_value').val()/2);
    });
});

// Validate form
function validateForm() {
    $("input, textarea, select").formError({remove: true});
    if (!validateMandatory()) return false;
    if (!validateType()) return false;
    if (!validateBussiness()) return false;
    // if (!validateBussiness2()) return false;
    return true;
}

// Validate for bussiness of fields
function validateBussiness2() {
    var tendency = parseFloat($('#indicators_tendency_value').val());
    var preparing = parseFloat($('#indicators_preparing_value').val());
    var exceed = parseFloat($('#indicators_exceed_value').val());
    if (!(tendency < preparing && tendency < exceed)){
        $("#indicators_tendency_value").formError(app.translate('ERR_Tendecy_Preparing_Exceed'));
        $('#indicators_tendency_value').focus();
        return false;
    }
     if (!(preparing < exceed)){
        $("#indicators_preparing_value").formError(app.translate('ERR_Tendecy_Preparing_Exceed'));
        $('#indicators_preparing_value').focus();
        return false;
    }
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

function resetForm() {
    // Todo
    return true;
}
