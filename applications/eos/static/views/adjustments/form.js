$(document).ready(function () {

    /*var current_created_date = $("#adjustments_created_date").val();
    var current_indicator_id_chosen = $("#select_adjustments_indicator_id").val();
    var current_adjustments_title = $("#adjustments_title").val();
     $("#adjustments_title").val(current_adjustments_title);
    $("#adjustments_created_date").val(current_created_date);
    $("#select_adjustments_indicator_id").val(current_indicator_id_chosen);
    console.log($("#adjustments_title").val());*/

    $("#adjustments_adjustment_type_chosen").prop({disabled: true});
    $("#adjustments_adjustment_type").prop({disabled: false});
    $("#adjustments_adjustment_type").prop({"style": "display: block"});
    $('#adjustments_adjustment_type_chosen').wrap('<fieldset id="new-block-2" hidden></fieldset>');
    $("#adjustments_submit_to").prop({disabled: false});
    $("#adjustments_submit_to").prop({"style": "display: block"});
    $('#adjustments_submit_to_chosen').wrap('<fieldset id="new-block-3" hidden></fieldset>');


    validator = $("form#frmMain").validate({

        rules: {
            station_id: 'required',
            created_date: 'required',
            title: 'required',
            from_date: 'required',
            to_date: 'required',
            adjustment_type: 'required',
            status: 'required',
        },
        messages: {}
    });
    var recordId = $('#hfStationId').val();
    if (recordId) {
        loadDataTableForPage();
        loadDataTableForPage_Indicator();
        loadDataTableForPage_camera();
    }

    if ($('#adjustments_logger_id').val() == '') {
        app.showConfirmBox({
            content: app.translate('JS_MSG_DATA_LOGGER'),
            callback: function () {
                pageURL = $(location).attr("href").split('/').slice(0, 3).join('/') + '/eos/datalogger/form';
                location.assign(pageURL);
                $('#f_logger_id_2').prop({disabled: false});
            }
        });
    }



    $('#btnSave').click(function () {

        if (!validateForm()) return;

        // If create new mode, 
        if ($('#hfMode').val() == '0') {
            // change "Draft" status to "Created"
            // $('#adjustments_status').val(1);
            // update "station_name"
            var sn = $("#adjustments_station_id option:selected").text();
            $('#adjustments_station_name').val(sn);
        }
        // update "indicator_name"
        var indicator_name = $("#adjustments_indicator_id option:selected").attr("value_db");
        $('#adjustments_indicator_name').val(indicator_name);

        // update "from_date"
        var from_date = $("#adjustments_from_date").val();
        if (from_date.length != 19) {
            $('#adjustments_from_date').val(from_date + ":00");
        }

        // update "to_date"
        var to_date = $("#adjustments_to_date").val();
        if (to_date.length != 19) {
            $('#adjustments_to_date').val(to_date + ":00");
        }

        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function () {
                $("#f_adjustments_created_date").prop({disabled: false});
                $("#select_adjustments_indicator_id").prop({disabled: false});
                $("#f_adjustments_title").prop({disabled: false});
                $("#f_adjustments_from_date").prop({disabled: false});
                $("#f_adjustments_to_date").prop({disabled: false});
                $("#adjustments_adjustment_type_chosen").prop({disabled: false});
                $("#f_submit_to").prop({disabled: false});
                $("#f_logger_id").prop({disabled: false});
                $("#f_indicator_value_1").prop({disabled: false});
                $("#f_indicator_value_2").prop({disabled: false});
                $("#f_tolerance_value").prop({disabled: false});
                $("#f_adjustments_adjustment_type").prop({disabled: false});

                $('#frmMain').submit();
            }
        });
    });
    
    $('#select_adjustments_indicator_id').on('change', function () {
        if ($('#select_adjustments_indicator_id option:selected').val() != '-- Chọn thông số --') {
           $('#adjustments_title').val('Hiệu chuẩn '+ $('#select_adjustments_indicator_id option:selected').text().split(' ')[0]);
        }
        else {
            $('#adjustments_title').val('');
        }

    });

    $('body').on('change', '#adjustments_station_id', function (e) {
        var station_id = $("#adjustments_station_id").val();
        var url = $(this).data('url');
        var data = {station_id: station_id};
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $('#adjustments_indicator_id').empty().append($("<option></option>")
                        .text('-- Chọn thông số --'));
                    $.each(res.station_indicator_list, function (key, value) {
                        var value_option = value.id;
                        var textName = value.indicators_name != null ? value.indicators_name : '-';
                        var textEnv = value.unit != null ? value.unit : '-';
                        $('#adjustments_indicator_id').append($("<option></option>")
                            .attr("value", value_option.toString())
                            .attr("value_db", textName.toString())
                            .text(textName + "(" + textEnv + ")"));
                    });
                    $("#adjustments_indicator_id").chosen().trigger("chosen:updated");
                    // $("#cbbQCVN_TYPE_CODE").selectpicker("refresh");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });
})
;

// Validate form
function validateForm() {
    if (!validateMandatory()) return false;
    if (!validateType()) return false;
    if (!validateBussiness()) return false;

    return true;
}

// Validate for fields mandatory
function validateMandatory() {
    if (!validator.form()) return false;
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
