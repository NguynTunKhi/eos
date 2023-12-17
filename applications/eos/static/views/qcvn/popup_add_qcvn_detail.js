/**
 * Created by Admin on 8/2/2017.
 */

$(document).ready(function() {
    app.registerEventsForCommonInput();

    $('.chosen-container-single').css('width', '100%');
    
    if ($('#hfQCVNId').val() != '') {
        var temp = $('#hfQCVNId').val();
        $('#qcvn_detail_qcvn_id').val(temp);
        $('#qcvn_detail_qcvn_id').trigger("chosen:updated");
    }
    
    $.validator.addMethod("requiredSelect", function(element) {
        return ( $("#qcvn_detail_qcvn_id :selected").val() != '');
    }, "You must select an option.");
            
    $('#btn_SaveEquip').click(function() {
        $("#frmPopupAddQCVN").validate({
            rules: {
                equipment: {required: true,},
                qcvn_id: {requiredSelect: false,},
            },
            messages: {
                equipment: app.translate('LBL_INPUT_MANDATORY_FIELD'),
                qcvn_id: app.translate('LBL_INPUT_MANDATORY_FIELD'),
            },
            submitHandler: function (form) {
                if(!validateBussiness()){
                    return false;
                }
                if ($("#qcvn_detail_qcvn_id :selected").val() == '') {
                    app.showError("Please select Station!");
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
        $("#frmPopupAddQCVN").submit();
    });
    
});

function validateBussiness() {
    return true;
}