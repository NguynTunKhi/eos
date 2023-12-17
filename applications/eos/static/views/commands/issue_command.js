$(document).ready(function() {
    
    $("#btn_Save").click(function() {
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_ISSUE_COMMAND'),
            callback: function () {
                $('.btnSave').trigger( "click" );
            }
        });
    });
    

});

