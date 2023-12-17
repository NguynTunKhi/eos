/**
 * Created by Admin on 8/2/2017.
 */

$(document).ready(function() {
    validator = $("form#frmAddFtp").validate({
        rules: {
            ftp_user: 'required',
            ftp_password: 'required',
            ftp_ip: 'required',
            ftp_port: 'required',
        },
        messages: {
            ftp_user: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            ftp_password: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            ftp_ip: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            ftp_port: app.translate('LBL_INPUT_MANDATORY_FIELD'),
        }
    });


   $('#btnSave').click(function() {
        if(!validator.form()) return
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function () {
                $('#frmAddFtp').submit();
            }
        });
    });
    $('body').on('click', '#btnCheckFTP', function (e) {
        var data = {
            ftp_user: $('#ftp_management_ftp_user').val(),
            ftp_password: $('#ftp_password').val(),
            ftp_ip: $('#ftp_management_ftp_ip').val(),
            ftp_port: $('#ftp_management_ftp_port').val(),
            administration_level: $('ftp_administration_level').val(),
        };
        if ((data.ftp_user != '') & (data.ftp_password  != '')
            & (data.ftp_ip  != '') & (data.ftp_port  != '')) {
            var url = $(this).data('url');
            app.postAjax({
                url: url,
                data: data,
                callback: function (res) {
                    if (res.success) {
                        app.showConfirmBox({
                            content: res.message,
                            callback: function () {
                            }
                        });
                    }
                }
            });
        } else {
            app.showError(app.translate('LBL_IN_PUT_ALL'));
        }
    });
});
