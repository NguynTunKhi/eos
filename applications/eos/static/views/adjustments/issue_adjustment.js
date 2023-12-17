$(document).ready(function() {

    $("#btn_Save").click(function() {
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_ISSUE_COMMAND'),
            callback: function () {
                $('.btnSave').trigger( "click" );

            }
        });
    });
    console.log('ready');
     $('#f_status_chosen').prop("style","width: 100px !important;");
    $('#f.status').prop('style','width: 100px');
    $('body').on('load', function () {


        console.log('run');
    });

});

