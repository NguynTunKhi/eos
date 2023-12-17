/**
 * Created by Admin on 8/8/2017.
 */

var _validFileExtensions = [".jpg", ".jpeg", ".bmp", ".gif", ".png"];

$(document).ready(function() {
    $('#password_again').val($('#usr_password').val());

    if ($('#usr_salary_level').val()) {
        $('#usr_salary_level_tmp').val($('#usr_salary_level').val());
    }

    if ($('#usr_salary').val()) {
        $('#usr_salary_tmp').val($('#usr_salary').val());
    }

    if ($('#usr_insurance').val()) {
        $('#usr_insurance_tmp').val($('#usr_insurance').val());
    }

    $('#usr_salary_level_tmp').number(true, 2);
    $('#usr_salary_tmp').number(true, 2);
    $('#usr_insurance_tmp').number(true, 2);

    $("form#form_usr").validate({
        rules: {
            lastname: "required",
            firstname: "required",
            email: "required",
            username: "required",
            password: {
                required: true,
                minlength: 6
            },
            password_again: {
                required: true,
                minlength: 6,
                equalTo: "#usr_password"
            },
        },
        messages: {
            lastname: "Hãy nhập họ tên!",
            firstname: "Hãy nhập tên!",
            email: "Hãy nhập email!",
            username: "Hãy nhập tài khoản người dùng!",
            password: {
                required: "Hãy nhập mật khẩu",
                minlength: "Mật khẩu cần có độ dài ít nhất 6 ký tự!"
            },
            password_again: {
                required: "Hãy nhập mật khẩu",
                minlength: "Mật khẩu cần có độ dài ít nhất 6 ký tự!",
                equalTo: "Mật khẩu không khớp!"
            },
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
    var oInput = document.getElementById('usr_image');
    if (oInput.type == "file") {
        var sFileName = oInput.value;
        if (sFileName.length > 0) {
            var blnValid = false;
            for (var j = 0; j < _validFileExtensions.length; j++) {
                var sCurExtension = _validFileExtensions[j];
                if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                    blnValid = true;
                    break;
                }
            }

            if (!blnValid) {
                app.showError(app.translate('MSG_ONLY_INPUT_IMAGE_FOR_THIS_FIELD'));
                return false;
            }
        }
    }
    return true;
}