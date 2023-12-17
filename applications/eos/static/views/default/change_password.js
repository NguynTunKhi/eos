$(document).ready(function() {
    validator = $(".change_password form").validate({
        rules: {
            old_password: {
                required: true,
            },
            new_password: {
                required: true,
            },
            new_password2: {
                required: true,
                equalTo: '#no_table_new_password',
            },
        },
        messages: {
        }
    });

    $('#btnSave').click(function() {
        if (!validateForm()) return;
        $('.change_password form').submit();
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