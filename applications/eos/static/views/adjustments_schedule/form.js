$(document).ready(function() {
    $("#optionsRadiosDaily").attr('checked', 'true');
    var url = window.location.href;
    var calendar_id = url.split("/").pop()
    if (calendar_id !== 'form')
        load_detail(calendar_id);
    validator = $("form#frmMain").validate({
        rules: {
            station_id: 'required',
            created_date: 'required',
            title: 'required',
            from_date: 'required',
            to_date: 'required',
            adjustment_type: 'required',
            status: 'required',
            start_time: 'required',
            end_time: 'required',
        },
        messages: {
        }
    });
    var recordId = $('#hfStationId').val();
    if (recordId) {
        loadDataTableForPage();
        loadDataTableForPage_Indicator();
        loadDataTableForPage_camera();
    }

    $('#btnSave').click(function() {
        if (!validateForm()) return;

        // If create new mode,
        if ($('#hfMode').val() == '0') {
            // change "Draft" status to "Created"
            // $('#adjustments_status').val(1);
            // update "station_name"
            var sn = $("#adjustments_calendar_station_id option:selected").text();
            $('#adjustments_calendar_station_name').val(sn);
        }
        // update "indicator_name"
        var indicator_name  = $("#adjustments_calendar_indicator_id option:selected").attr("value_db");
        $('#adjustments_calendar_indicator_name').val(indicator_name);

        // update "from_date"
        var from_date  = $("#adjustments_calendar_from_date").val();
        if (from_date.length != 19) {
            $('#adjustments_calendar_from_date').val(from_date  + ":00");
        }

        // update "to_date"
        var to_date  = $("#adjustments_calendar_to_date").val();
        if (to_date.length != 19) {
            $('#adjustments_calendar_to_date').val(to_date  + ":00");
        }

        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function() {
                $('#frmMain').submit();
            }
        });
    });

    $('#adjustments_calendar_indicator_id').on('change', function () {
        if ($('#adjustments_calendar_indicator_id option:selected').val() != '-- Chọn thông số --') {
            $('#adjustments_calendar_title').val('Hiệu chuẩn '+ $('#adjustments_calendar_indicator_id option:selected').text().split('(')[0]);
        }
        else {
            $('#adjustments_calendar_title').val('');
        }
    });

    $('#adjustments_calendar_station_id').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {station_id: $('#adjustments_calendar_station_id').val()},
            callback: function (res) {
                if (res.success) {
                    $('#adjustments_calendar_logger_id').val(res.logger_id);
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('body').on('change', '#adjustments_calendar_station_id', function (e) {
        $('#adjustments_calendar_title').val('');
        var station_id = $("#adjustments_calendar_station_id").val();
        var url = $(this).data('url');
        var data = {station_id: station_id};
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $('#adjustments_calendar_indicator_id').empty().append($("<option></option>")
                                        .text('-- Chọn thông số --'));
                    $.each(res.station_indicator_list, function (key, value) {
                        var value_option = value.id;
                        var textName = value.indicators_name != null ? value.indicators_name : '-';
                        var textEnv = value.unit != null ? value.unit : '-';
                           $('#adjustments_calendar_indicator_id').append($("<option></option>")
                                        .attr("value",value_option.toString())
                                        .text(textName + "(" + textEnv + ")"));
                    });
                    $("#adjustments_calendar_indicator_id").chosen().trigger("chosen:updated");
                    // $("#cbbQCVN_TYPE_CODE").selectpicker("refresh");
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
});

// Validate form
function validateForm() {
    if (!validateMandatory()) return false;
    if (!validateType()) return false;
    if (!validateBussiness()) return false;

    return true;
}

// Validate for fields mandatory
function validateMandatory() {
    if(!validator.form()) return false;
    return true;
}

// Validate for type of fields
function validateType() {
    return true;
}

// Validate for bussiness of fields
function validateBussiness() {
    // Todo
    return true;
}
function load_detail(calendar_id) {
    url = $("#hfCalendarId").val();
    app.postAjax({
        url: url,
        data: {calendar_id: calendar_id},

        callback: function (res) {
            if (res.success) {
                // var data = res.data;
                $('#start_time').val(res.start_hour);
                $('#end_time').val(res.end_hour);

                if (res.data.frequency === 'weekly') {
                    // $("#weeklyFrequency").val(data.frequency_at);
                    $("#optionsRadiosWeekly").prop("checked", true);
                    $("#weeklyFrequency").html(res.freq_html)
                    $('#weeklyFrequency').trigger("chosen:updated");
                }
                if (res.data.frequency === 'monthly') {
                    // $("#weeklyFrequency").val(data.frequency_at);
                    $("#optionsRadiosMonthly").prop("checked", true);
                    $("#monthlyFrequency").html(res.freq_html)
                    $('#monthlyFrequency').trigger("chosen:updated");
                }
            } else {
                app.showError(res.message);
            }
        }
    });
}