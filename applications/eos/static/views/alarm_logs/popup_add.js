
$(document).ready(function() {
    app.registerEventsForCommonInput();

    $('.chosen-container-single').css('width', '100%');
    
    $("form#frmPopupAddAlarmLog").validate({
        rules: {
            content: "required",
        },
        submitHandler: function (form) {
            if(!validateBussinessPopupAddAlarmlog()){
                return false;
            }
            app.showConfirmBox({
                content: app.translate('JS_MSG_CONFIRM_SAVE'),
                callback: function () {
                    $('.btnSave').trigger( "click" );
                    loadNotification();
                }
            });
        }
    });

    $('body').on('change', '#alarm_logs_station_id', function (e) {
        // Update station name
        alpa_updateStationName();
    });

    $('body').on('click', '#alarm_logs_send_sms', function (e) {
        // Show hide phone field
        alpa_showHidePhoneField();
    });

    $(".ModalWrap > .modal > .modal-content").draggable({
        handle: ".modal-header"
    });

    // Update station name
    alpa_updateStationName();

    // Show hide phone field
    alpa_showHidePhoneField();

    $('.btn_SaveAlarmLog').click(function() {
        $("#frmPopupAddAlarmLog").submit(); 
    });
});

function loadNotification()
{   
    var url = $("#urlAlarmLogs_menu").val();
    var data = "";
    app.postAjax({
        url: url,
        data: {},
        callback: function (res) {
            if (res.success) {
                $('#alarm_menu').html(res.html_total);
                $('#alarm_logs_header').html(res.html);
                $('#station_alarm_menu').html(res.html_station_alarm);
                $('#station_inactive_menu').html(res.html_station_inactive);
                $('#indicator_alarm_menu').html(res.html_indicator_alarm);
                $('#not_solve_alarm_menu').html(res.html_not_solve_alarm);
                $('#equipment_error').html(res.html_equipment_error);
            } else {
                app.showError(res.message);
            }
        }
    });
}

function validateBussinessPopupAddAlarmlog() {
    return true;
}

function alpa_updateStationName() {
    var station_name = $('.ModalWrap #alarm_logs_station_id option:selected').text();
    $('.ModalWrap #alarm_logs_station_name').val(station_name);
}

function alpa_showHidePhoneField() {
    if ($('#alarm_logs_send_sms').prop('checked')){
        $('.ModalWrap .alarm_to_phone').show();
    } else {
        $('.ModalWrap .alarm_to_phone').hide();
    }
}