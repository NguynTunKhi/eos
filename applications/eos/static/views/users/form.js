/**
 * Created by Admin on 8/8/2017.
 */

$(document).ready(function() {
    validator = $("form#frmMain").validate({
        rules: {
            username:
            {
                required: true,
                username: true, 
            },
            first_name: 'required',
            last_name: 'required',
            email: {
                required: true,
                email: true,
            }, 
            phone: { 
                phone: true,
            },
            password: {
                required: function (element) {
                    return ($("#hfdRecordId").val() == "");
                }
            },
        },
        messages: {
            first_name: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            last_name: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            username: 
            {
                required : app.translate('LBL_INPUT_MANDATORY_FIELD'),
                username : app.translate('LBL_INPUT_USERNAME_FIELD'), 
            },
            email:
            {
                required : app.translate('LBL_INPUT_MANDATORY_FIELD'),
                email : app.translate('LBL_INPUT_EMAIL_FIELD'), 
            },
            phone: app.translate('LBL_INPUT_PHONE_FIELD'),  
        }
    });
    $('#password_again').val($('#usr_password').val());

    //validateForm();
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
function validateForm() {
    if (!validateMandatoryForm()) return false;
    return true;
}
/*function validateForm() {
    rules = {
        last_name: "required",
        first_name: "required",
        email: "required",
    };
    messages = {
        lastname: app.translate('LBL_PLEASE_ENTER_LASTNAME_FIELD'),
        firstname: app.translate('LBL_PLEASE_ENTER_FIRSTNAME_FIELD'),
        email: app.translate('LBL_PLEASE_ENTER_EMAIL_FIELD'),
        username: app.translate('LBL_PLEASE_ENTER_USERNAME_FIELD'),
    };

    $('form').data('validator', null);
    $("form").unbind('submit');
    $("form").unbind('validate');
    $("form").validate({
        rules: rules,
        messages: messages,
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
}*/
// Validate for fields mandatory
function validateMandatoryForm() { 
    // var birthdate = $('#auth_user_birthdate').val(); 
    // if (dt != '')
    // {
        // var currentDT = new Date(); 
        // var dt = new Date(birthdate);
        // if (dt >= currentDT){
            // app.showError(app.translate("MSG_BIRTHDATE_MUST_BE_GREATER_THAN_NOW"));
            // return false;
        // }
    // }
    if(!validator.form()) return false;
    return true;
}
function validateBussiness() {
    return true;
}