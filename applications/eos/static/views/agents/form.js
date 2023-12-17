$(document).ready(function() {
    var recordId = $('#hfAgentId').val();
    if (recordId) {
        loadDataTableForPage();
    }
    // See more: https://jqueryvalidation.org/documentation/
    validator = $("form#frmMain").validate({
        rules: {
            agent_name: 'required',
            province_id: 'required',
            manage_agent: 'required',
            // longitude: {
                // required: true,
                // number: true,
                // range: [7, 24],
            // },
            // latitude: {
                // required: true,
                // number: true,
                // range: [100, 112],
            // },
            order_number: 'digits',
            email: 'email',
            phone: 'phone',
            data_server_port: 'digits',
        },
        messages: {
            
        }
    });
    
    $('#btnSave').click(function() {
        if (!validateForm()){
            app.focusToFirstError();
            return false;
        }
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function() {
                $('#frmMain').submit();
            }
        });
    });


    // Add new Indicator to station
    $('body').on('click', '#btnLinkIndicatorToWaterStation', function (e) {
        if (!validateForm2()) return;
        var station_type = $(this).data('type');
        var data = {
            indicator: $('#cbbIndicatorId').val(),
            tendency: $('#txtTendency').val(),
            preparing: $('#txtPreparing').val(),
            exceed: $('#txtExceed').val(),
            station_id: $('#hfStationId').val(),
            station_name: $('#hfStationName').val(),
            equipment_id: $('#cbbEquipment').val(),
            equipment: $('#cbbEquipment option:selected').text(),
            qcvn_id: $('#cbbQCVN').val(),
            qcvn_code: $('#cbbQCVN option:selected').text(),
            indicator_name_mapping: $('#indicator_name_mapping').val(),
            convert_rate: $('#convert_rate').val(),
            station_type: station_type,
        };
        
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    oTable[1].fnDraw();
                } else {
                    app.showError(res.message);
                }
            }
        });
    });
});

// Validate form
function validateForm() {
    if (!validateMandatory()) return false;
    if (!validateBussiness()) return false;

    return true;
}


// Validate for fields mandatory
function validateMandatory() {
    if(!validator.form()) return false;
    return true;
}

// Validate for bussiness of fields
function validateBussiness() {
    // Todo
    return true;
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%'},
        {'sWidth' : '27%'},
        {'sWidth' : '30%'},
        {'sWidth' : '7%'},
        {'sWidth' : '15%'},
        {'sWidth' : '15%'},
        {'sWidth' : '3%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', 'text-left', 'text-left', 'text-left', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
    });
    
    return true;
}

function reloadDatatable() {
    oTable[0].fnDraw();
}
