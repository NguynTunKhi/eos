/**
 * Created by Admin on 8/2/2017.
 */

$(document).ready(function() {
    app.registerEventsForCommonInput();

    $("#frmPopupAddEquipment").validate({
        rules: {
            equipment: {required: true,},
            request_create_station_id: {required: true,},
            lrv: {number: true,},
            urv: {
                number: true,
                greaterOrEqual: 'lrv'},
            warranty_start: {
                date: true,},
            warranty_end: {
                greaterOrEqual: 'warranty_start',
                date: true,},
        },
        messages: {
        },
        submitHandler: function (form) {
            if(!validateBussiness()){
                return false;
            }
            if ($("#equipments_request_station_id :selected").val() == '') {
                app.showError("Please select Request Create Station!");
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

    $('.chosen-container-single').css('width', '100%');

    if ($('#hfRequestCreateStationId').val() != '') {
        var temp = $('#hfStationId').val();
        $('#equipments_request_station_id').val(temp);
        $('#equipments_request_station_id').trigger("chosen:updated");
    }

    $('#btn_SaveEquip').click(function() {
        $("#frmPopupAddEquipment").submit();
    });

});

function validateBussiness() {
    return true;
}