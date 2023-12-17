$(document).ready(function () {
    // See more: https://jqueryvalidation.org/documentation/
    validator = $("form#frmMain").validate({
        rules: {
            province_code: 'required',
            province_name: 'required',
            order_no: 'digits',
        }
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
    if (!validateBussiness()) return false;

    return true;
}

// Validate for fields mandatory
function validateMandatory() {
    if (!validator.form()) return false;
    return true;
}

// Validate for bussiness of fields
function validateBussiness() {
    // Todo
    var order_no = $('#provinces_order_no').val();
    order_no = parseInt(order_no);
    if (order_no < 0) {
        validator.showErrors({'order_no': app.translate('Not allow to negative value')});
        $('#provinces_order_no').focus();
        return false;
    }
    return true;
}
