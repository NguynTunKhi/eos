
$(document).ready(function() {
    app.registerEventsForCommonInput();

    $('.chosen-container-single').css('width', '100%');

    $("form#frmPopupConfigPublic").validate({
        rules: {
            content: "required",
        },
        submitHandler: function (form) {
            if(!validateBussinessfrmPopupConfigPublic()){
                return false;
            }
            app.showConfirmBox({
                content: app.translate('JS_MSG_CONFIRM_SAVE'),
                callback: function () {
                    $('.btnSave').trigger( "click" );
                }
            });
        }
    });

    $(".ModalWrap > .modal > .modal-content").draggable({
        handle: ".modal-header"
    });

    $('#check').click(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {public: $('#eip_config_time_public').val()},
            callback: function (res) {
                console.log(res)
                if (res.success) {
                    $('#infoPublic').html(res.html);
                    console.log(res.html)
                    $('#infoPublic').trigger("change");
                    $('#infoPublic').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
         $('#infoPublic').removeClass('hide');
    });

    $('.btn_SaveConfigPublic').click(function() {
        $("#frmPopupConfigPublic").submit();
    });
});

function validateBussinessfrmPopupConfigPublic() {
    return true;
}


