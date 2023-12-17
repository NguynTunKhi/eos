$(document).ready(function () {
    validator = $("form#frmMain").validate({
        rules: {
            qcvn_name: 'required',
            qcvn_code: 'required',
            qcvn_type: 'required',
        },
        messages: {}
    });

    validator_3 = $("form#frmMain").validate({
        rules: {
            indicator: {
                required: true,
            },
            qcvnMin: {
                number: true,
            },
            qcvnMax: {
                number: true,
            },
        },
        messages: {}
    });

    var qcvnId = $('#hfQCVNId').val();
    if (qcvnId) {
        // loadDataTableForPage();
        loadDataTableForPage_Kink();
        loadDataTableForPage_Indicator();
    }

    $('#btnSave').click(function () {
        if (!validateForm()) return;
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function () {
                $('#frmMain').submit();
            }
        });
    });
    // Fill URV, LRV cua Equipment khi dropdown thay doi
    $('body').on('change', '#cbbIndicatorId', function (e) {

        var tendency = $(this).find(':selected').data('tendency');
        var preparing = $(this).find(':selected').data('preparing');
        var exceed = $(this).find(':selected').data('exceed');

        // Set value to textbox
        $('#txtTendency').val(tendency);
        $('#txtPreparing').val(preparing);
        $('#txtExceed').val(exceed);

    });

    // expression qcvn indicator change
    $('body').on('change', '#txtExpressionQcvnIndicator', function (e) {
        var expression_qcvn_indicator = $(this).find(':selected').val();

        if (expression_qcvn_indicator == '') {
            $("#txtQcvnMax").attr("type", "hidden");
            $("#lblTxtQcvnMax").attr("style", "Display: none;");
            $("#txtQcvnMax").val();
            $("#txtQcvnMin").attr("type", "hidden");
            $("#lblTxtQcvnMin").attr("style", "Display: none;");
            $("#txtQcvnMin").val();
        } else if (expression_qcvn_indicator == 2) {

            $("#txtQcvnMax").attr("type", "number");
            $("#txtQcvnMax").prop({
                disabled: true
            });
            $("#txtQcvnMin").prop({
                disabled: false
            });

            $("#lblTxtQcvnMax").attr("style", "Display: block;");
            $("#txtQcvnMax").val(' ');
            $("#txtQcvnMin").attr("type", "number");
            $("#lblTxtQcvnMin").attr("style", "Display: block;");
        } else if (expression_qcvn_indicator == 1) {

            $("#txtQcvnMin").attr("type", "number");
            $("#txtQcvnMin").prop({
                disabled: true
            });
            $("#txtQcvnMax").prop({
                disabled: false
            });
            $("#lblTxtQcvnMin").attr("style", "Display: block;");
            $("#txtQcvnMin").val(' ');
            $("#txtQcvnMax").attr("type", "number");
            $("#lblTxtQcvnMax").attr("style", "Display: block;");

        } else if (expression_qcvn_indicator == 3) {
            $("#txtQcvnMax").prop({
                disabled: false

            });
            $("#txtQcvnMin").prop({
                disabled: false
            });
            $("#txtQcvnMin").attr("type", "number");
            $("#lblTxtQcvnMin").attr("style", "Display: block;");
            $("#txtQcvnMax").attr("type", "number");
            $("#lblTxtQcvnMax").attr("style", "Display: block;");
        }
    });
    $('body').on('change', '#txtHaveFactorIndicator', function (e) {
        var have_factor_qcvn = $(this).find(':selected').val();
    });

    // Add new Indicator to station
    $('body').on('click', '#btnLinkIndicatorToWaterStation', function (e) {
        $("input, textarea, select").formError({remove: true});
        // if(!validator_3.form()) return false;

        if ($('#cbbIndicatorId').val() == '') {
            $("#cbbIndicatorId").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
            $('#cbbIndicatorId').focus();
            return false;
        }
        var expression_qcvn_indicator = $('#txtExpressionQcvnIndicator').find(':selected').val();
        var have_factor_qcvn = $('#txtHaveFactorIndicator').find(':selected').val();
        if (expression_qcvn_indicator == 2) {
            if ($('#txtQcvnMin').val() == '') {
                $("#txtQcvnMin").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
                $('#txtQcvnMin').focus();
                return false;
            }
        } else if (expression_qcvn_indicator == 1) {
            if ($('#txtQcvnMax').val() == '') {
                $("#txtQcvnMax").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
                $('#txtQcvnMax').focus();
                return false;
            }
        } else if (expression_qcvn_indicator == 3) {
            if ($('#txtQcvnMax').val() == '' || $('#txtQcvnMin').val() == '') {
                $("#txtQcvnMax").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
                $('#txtQcvnMax').focus();

                $("#txtQcvnMin").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
                $('#txtQcvnMin').focus();
                return false;
            }
            var txtQcvnMin = parseFloat($('#txtQcvnMin').val());
            var txtQcvnMax = parseFloat($('#txtQcvnMax').val());
            if (!(txtQcvnMin < txtQcvnMax)) {
                $("#txtQcvnMax").formError(app.translate('JS_MSG_txtQcvnMin_less_txtQcvnMax'));
                $('#txtQcvnMax').focus();
                return false;
            }
        }
        var qcvn_type = $(this).data('type');
        var data = {
            indicator: $('#cbbIndicatorId').val(),
            tendency: $('#txtTendency').val(),
            preparing: $('#txtPreparing').val(),
            exceed: $('#txtExceed').val(),
            qcvn_id: $('#hfQCVNId').val(),
            qcvn_name: $('#hfQCVNName').val(),
            qcvn_code: $('#hfQCVNCode').val(),
            qcvn_type: qcvn_type,
            qcvn_type_code: $('#txtQcvnTypeCode').val(),
            qcvn_min_value: $('#txtQcvnMin').val(),
            qcvn_max_value: $('#txtQcvnMax').val(),
            qcvn_const_area_value: $('#txtQcvnConstArea').val(),
            submit_type: 0, // Check exit
            expression_qcvn_indicator: expression_qcvn_indicator,
            have_factor_qcvn: have_factor_qcvn,
        };
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    if (res.success_type == 1) {

                        app.showConfirmBox({
                            title: app.translate('LBL_ALERT'),
                            content: app.translate('JS_MSG_CONFIRM_UPDATE'),
                            callback: function () {
                                data["submit_type"] = 1;
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
                            }
                        });
                    }
                    oTable[1].fnDraw();
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    // Add new Indicator to station
    $('body').on('click', '#btnLinkKinkToWaterStation', function (e) {
        if (!validateForm3()) return;
        var qcvn_type = $(this).data('type');
        console.log($('#hfQCVNId').val());
        var data = {
            qcvn_id: $('#hfQCVNId').val(),
            qcvn_name: $('#hfQCVNName').val(),
            qcvn_code: $('#hfQCVNCode').val(),
            qcvn_type: qcvn_type,
            qcvn_kind: $('#txtqcvn_kind').val(),
            qcvn_kind_order: $('#txtqcvn_kind_order').val()
        };
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    oTable[2].fnDraw();
                    location.reload();
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

});

// Validate for Indicator expression


// Validate form Indicator
function validateForm2() {
    $("input, textarea, select").formError({remove: true});
    if (!validateMandatory2()) return false;
    if (!validateType2()) return false;
    if (!validateBussiness2()) return false;

    return true;
}

// Validate form Indicator
function validateForm3() {
    $("input, textarea, select").formError({remove: true});
    if (!validateMandatory3()) return false;

    return true;
}

// Validate for fields mandatory
function validateMandatory2() {
    if (!$('#cbbIndicatorId').val().trim()) {
        $("#cbbIndicatorId").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
        $('#cbbIndicatorId').focus();
        return false;
    }
    if (!$('#txtTendency').val().trim()) {
        $("#txtTendency").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
        $('#txtTendency').focus();
        return false;
    }
    if (!$('#txtPreparing').val().trim()) {
        $("#txtPreparing").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
        $('#txtPreparing').focus();
        return false;
    }
    if (!$('#txtExceed').val().trim()) {
        $("#txtExceed").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
        $('#txtExceed').focus();
        return false;
    }
    // if (!$('#txtQcvnTypeCode').val().trim()) {
    //     $("#txtQcvnTypeCode").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
    //     $('#txtQcvnTypeCode').focus();
    //     return false;
    // }
    // if (!$('#txtQcvnMin').val().trim()) {
    //     $("#txtQcvnMin").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
    //     $('#txtQcvnMin').focus();
    //     return false;
    // }
    if (!$('#txtQcvnMax').val().trim()) {
        $("#txtQcvnMax").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
        $('#txtQcvnMax').focus();
        return false;
    }
    // if (!$('#txtQcvnConstArea').val().trim()) {
    //     $("#txtQcvnConstArea").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
    //     $('#txtQcvnConstArea').focus();
    //     return false;
    // }
    return true;
}

// Validate for fields mandatory
function validateMandatory3() {
    if (!$('#txtqcvn_kind').val().trim()) {
        $("#txtqcvn_kind").formError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
        $('#txtqcvn_kind').focus();
        return false;
    }

    return true;
}

// Validate for type of fields
function validateType2() {
    return true;
}

// Validate for bussiness of fields
function validateBussiness2() {
    var tendency = parseFloat($('#txtTendency').val());
    var preparing = parseFloat($('#txtPreparing').val());
    var exceed = parseFloat($('#txtExceed').val());
    if (!(tendency < preparing && preparing < exceed)) {
        $("#txtTendency").formError(app.translate('Tendecy < Preparing < Exceed'));
        $('#txtTendency').focus();
        return false;
    }

    var txtQcvnMin = parseFloat($('#txtQcvnMin').val());
    var txtQcvnMax = parseFloat($('#txtQcvnMax').val());
    if (!(txtQcvnMin < txtQcvnMax)) {
        $("#txtQcvnMax").formError(app.translate('JS_MSG_txtQcvnMin_less_txtQcvnMax'));
        $('#txtQcvnMax').focus();
        return false;
    }
    return true;
}

function loadDataTableForPage_Indicator() {
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [
        {'sWidth': '5%'},
        {'sWidth': '15%'},
        {'sWidth': '15%'},
        {'sWidth': '10%'},
        {'sWidth': '20%'},
        {'sWidth': '15%'},
        {'sWidth': '15%'},
        {'sWidth': '5%'},
    ];

    var aoClass = ['', 'text-left', '', '', '', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        // sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "qcvn_id", "value": $('#hfQCVNId').val()
            });
        },
        iTable: 1
    });

    return true;
}

function loadDataTableForPage_Kink() {
    var sAjaxSource = $("#custom_datatable_2").attr("data-url");
    var aoColumns = [
        {'sWidth': '5%'},
        {'sWidth': '45%'},
        {'sWidth': '15%'},
        {'sWidth': '5%'},
    ];

    var aoClass = ['', 'text-left', '', '', '', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "qcvn_id", "value": $('#hfQCVNId').val()
            });
        },
        iTable: 2
    });

    return true;
}

// Validate form
function validateForm() {
    $("input, textarea, select").formError({remove: true});
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

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth': '3%'},
        {'sWidth': '20%'},
        {'sWidth': '10%'},
        {'sWidth': '25%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '8%'},
    ];

    var aoClass = ['', 'text-left', '', 'text-left', '', '', 'text-right'];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
    });

    return true;
}

function reloadDatatable_QCVNDetail() {
    oTable[0].fnDraw();
} 