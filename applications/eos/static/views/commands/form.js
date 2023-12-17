$(document).ready(function () {
    // Filter station by type when dropdown station_type changed
    validator = $("form#frmMain").validate({
        rules: {
            // station_type: 'required',
            station_id: 'required',
            // equipment_id: 'required',
            bottle: {
                required: true,
                digits: true,
            },
            title: 'required',
            command: 'required',
            logger_id: 'required',
            type_logger: 'required',
        },
        messages: {}
    });
    $('#commands_station_type').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {filter_value: $(this).val()},

            callback: function (res) {
                if (res.success) {
                    $('#commands_station_id').html(res.html);
                    $('#commands_station_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    if ($('#commands_station_type option:selected').val() == '') {
        var url = $('#commands_station_type').data('url');
        console.log(url);
        app.postAjax({
            url: url,
            data: {filter_value: $(this).val()},

            callback: function (res) {
                if (res.success) {
                    $('#commands_station_id').html(res.html);
                    $('#commands_station_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    }

    $('#commands_station_id').change(function () {
        var url = $('#hfUrl2').val();
        app.postAjax({
            url: url,
            data: {
                filter_value: $(this).val(),
                station_id: $('#commands_station_id').val()
            },

            callback: function (res) {
                if (res.success) {
                    if ($('#command_id option:selected').val() != '') {
                        $('#commands_command').val('');
                    }
                    $('#commands_logger_id').val(res.logger_id);
                    $('#commands_type_logger').val(res.type_logger);
                    $('#command_id').html(res.html);
                    $('#command_id').trigger("chosen:updated");
                    $('#cbbTypeLogger').val(res.type_logger);
                    $('#cbbTypeLogger').trigger("chosen:updated");
//                    var element = "<div class='row form-group'><label class='col-sm-6 col-md-2' for='commands_title'>{{=T('No of bottles')}} <span style='color:red;'>*</span></label><div class='col-sm-6 col-md-4'>{{=f.bottle}}</div></div>"
//                    $('#testAppen').append(element);
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('#command_id').change(function () {
        var url = $('#hfUrl2').val();
        app.postAjax({
            url: url,
            data: {
                filter_value: $(this).val(),
                command_id: $('#command_id option:selected').val()
            },

            callback: function (res) {
                if (res.success) {
                    if (res.type_logger == 'ADAM') {
                        $('#commands_command').val(res.command_name);
                    } else {
                        $('#commands_command').val(res.command_content);
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('#btnSave').click(function () {

        if ($('#commands_station_name').val() == '') {       // Neu la create new
            var station_name = $('#commands_station_id option:selected').text();
            $('#commands_station_name').val(station_name);
        }
        if ($('#commands_title').val() == '') {       // Neu la create new
            var commands_title = $('#command_id option:selected').text();
            $('#commands_title').val(commands_title);
        }
        if (!validateForm()) return;
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function () {
                $('#frmMain').submit();
            }
        });
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

function resetForm() {
    // Todo
    return true;
}
