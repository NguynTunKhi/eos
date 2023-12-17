$(document).ready(function () {
    var url = window.location.href;
    var calendar_id = url.split("/").pop()
    if (calendar_id !== 'form')
        load_detail(calendar_id);
    $('#btnSetSchedule').click(function () {
        if (validate()) {
            app.showError(validate());
            return false;
        }
        ;
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SET_SCHEDULE_COMMAND'),
            callback: function () {
                var current_url = window.location.href;
                var calendar_id = current_url.split("/").pop()
                var data = {
                    calendar_id: calendar_id,
                    command_id: $('#command_id').val(),
                    logger_id: $('#command_logger_id').val(),
                    bottle: $('#command_bottle').val(),
                    content: $('#command').val(),
                    repeat_mode: $("input[name='repeatMode']:checked").val(),
//                    start_time: $("#start_time").val(),
//                    end_time: $("#end_time").val(),
                    start_date: $("#start_date").val(),
                    end_date: $("#end_date").val(),
//                    weeklyFrequency: $("#weeklyFrequency").val().toString(),
//                    monthlyFrequency: $("#monthlyFrequency").val().toString(),
                };
                var url = $('#btnSetSchedule').data('url');
                app.postAjax({
                    url: url,
                    data: data,
                    callback: function (res) {
                        if (res.success) {
                            swal({
                                    title: app.translate('Schedule set successful'),
                                    type: "success",
                                    confirmButtonColor: "green",
                                    confirmButtonText: "OK",
                                    closeOnConfirm: false,
                                },
                                function (isConfirm) {
                                    if (isConfirm) {
                                        // location.reload();
                                        window.location.href = $("#indexUrl").val();
                                    }
                                });
                            // window.location.href = 'index';

                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });

    // Set dropdown selected (khi tu man hinh command list click 'set schedule'
    var commandId = $('#hfCommandId').val();
    if (commandId != '') {
        $("#command_id").val(commandId).change();
        $('#command_id').trigger("chosen:updated");

        // Get command content
        var url = $('#command_id').data('url');
        app.postAjax({
            url: url,
            data: {command_id: commandId},

            callback: function (res) {
                if (res.success) {
                    $('#command').val(res.command);
                } else {
                    app.showError(res.message);
                }
            }
        });
    }

    // Update Dropdown content of selected station
    $('#station_id').change(function () {
        var url = $(this).data('url');
        var data = {};
        app.postAjax({
            url: url,
            data: {filter_value: $('#station_id').val().trim()},

            callback: function (res) {
                if (res.success) {
                    $('#command_id').html(res.html);
                    $('#command_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });
    // Update textarea content of selected command
    $('#command_id').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {command_id: $(this).val()},

            callback: function (res) {
                if (res.success) {
                    $('#command').val(res.command);
                    $('#command_logger_id').val(res.datalogger_id);
                    // $('#station_id').html(res.stations_html);
                    $('#station_id').val(res.station_id);
                    $('#station_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });
    $('#start_time').datetimepicker({
        datepicker: false,
        format: 'H:i'
    });
    $('#end_time').datetimepicker({
        datepicker: false,
        format: 'H:i'
    });
    $("#optionsRadiosDaily").attr('checked', 'true');

});


function validate() {
    var data = {
        command_id: $('#command_id').val(),
        repeat_mode: $("input[name='repeatMode']:checked").val(),
        bottle: $('#command_bottle').val(),
        content: $('#command').val(),
//        start_time: $("#start_time").val(),
//        end_time: $("#end_time").val(),
        start_date: $("#start_date").val(),
        end_date: $("#end_date").val(),
//        weeklyFrequency: $("#weeklyFrequency").val().toString(),
//        monthlyFrequency: $("#monthlyFrequency").val().toString(),
    };
    if (!data.command_id) return app.translate('JS_MSG_ERROR_COMMAND_ID_REQUIRED');
    if (!data.bottle) return app.translate('JS_MSG_ERROR_COMMAND_ID_REQUIRED');
    if (!data.content) return app.translate('JS_MSG_ERROR_COMMAND_ID_REQUIRED');
//    if (!data.start_time) return app.translate('JS_MSG_ERROR_START_TIME_REQUIRED');
//    if (!data.end_time) return app.translate('JS_MSG_ERROR_END_TIME_REQUIRED');
    if (!data.start_date) return app.translate('JS_MSG_ERROR_START_DATE_REQUIRED');
    if (!data.end_date) return app.translate('JS_MSG_ERROR_END_DATE_REQUIRED');
//    if (data.reapeat_mode === 'weekly')
//        if (!data.weeklyFrequency) return app.translate('JS_MSG_ERROR_WEEKLY_REQUIRED');
//    if (data.reapeat_mode === 'monthly')
//        if (!data.monthlyFrequency) return app.translate('JS_MSG_ERROR_MONTHLY_REQUIRED');
    if (data.start_date > data.end_date) return app.translate('JS_MSG_ERROR_DATE_STARTEND_REQUIRED');
    if (data.start_time > data.end_time) return app.translate('JS_MSG_ERROR_TIME_STARTEND_REQUIRED');
    return "";
}

function load_detail(calendar_id) {
    url = $("#hfCalendarId").val();
    app.postAjax({
        url: url,
        data: {calendar_id: calendar_id},

        callback: function (res) {
            if (res.success) {
                // var data = res.data;
                $('#station_id').val(res.data.station_id);
                $('#station_id').trigger("chosen:updated");

                $('#command_id').val(res.data.command_id);
                $('#command_id').trigger("chosen:updated");

                $('#command_bottle').val(res.data.bottle);
                $('#command_logger_id').val(res.datalogger_id);
                $('#command').val(res.data.content);

//                $('#start_time').val(res.start_hour);
//                $('#end_time').val(res.end_hour);
                $('#start_date').val(res.start_date);
                $('#end_date').val(res.end_date);

//                if (res.data.frequency === 'weekly') {
//                    // $("#weeklyFrequency").val(data.frequency_at);
//                    $("#optionsRadiosWeekly").prop("checked", true);
//                    $("#weeklyFrequency").html(res.freq_html)
//                    $('#weeklyFrequency').trigger("chosen:updated");
//                }
//                if (res.data.frequency === 'monthly') {
//                    // $("#weeklyFrequency").val(data.frequency_at);
//                    $("#optionsRadiosMonthly").prop("checked", true);
//                    $("#monthlyFrequency").html(res.freq_html)
//                    $('#monthlyFrequency').trigger("chosen:updated");
//                }
                // $('#command_id').val(res.command_id);
                //         repeat_mode: $("input[name='repeatMode']:checked").val(),
                // bottle: $('#command_bottle').val(),
                // content: $('#command').val(),
                // start_time: $("#start_time").val(),
                // end_time: $("#end_time").val(),
                // start_date: $("#start_date").val(),
                // end_date: $("#end_date").val(),
                // weeklyFrequency: $("#weeklyFrequency").val().toString(),
                // monthlyFrequency: $("#monthlyFrequency").val().toString(),
            } else {
                app.showError(res.message);
            }
        }
    });
}