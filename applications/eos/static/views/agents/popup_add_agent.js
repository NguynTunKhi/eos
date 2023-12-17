/**
 * Created by Admin on 8/2/2017.
 */

$(document).ready(function() {
    app.registerEventsForCommonInput();
    
    $('.chosen-container-single').css('width', '100%');
    
    
    $('body').on('change', '#receive_agent', function(e){
        var url = $(this).data('url');
        var agent_id = $(this).val();
        var data = {agent_id: agent_id};
        
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $('#data_server').val(res.agent.data_server);
                    $('#data_server_port').val(res.agent.data_server_port);
                    $('#directory_format').val(res.agent.directory_format);
                    $('#file_format').val(res.agent.file_format);
                    $('#username').val(res.agent.username);
                    $('#pwd').val(res.agent.pwd);
                } else {
                    app.showError(res.message);
                }
            }
        });
    });
    
    $("form#frmPopupAddAgent").validate({
        rules: {
            receive_agent: "required",
        },
        messages: {
            receive_agent: app.translate('LBL_INPUT_MANDATORY_FIELD'),
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
    return true;
}