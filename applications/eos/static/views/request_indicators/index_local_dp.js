var cols = [
    {data: 'id_int', 'sWidth': '10%', 'bSort': false},
    {data: 'indicator', 'sWidth': '10%', 'bSortable': false},
    {
        data: 'indicator_type', 'sWidth': '10%', 'bSortable': false,
        render: function (data, type) {
            if (data == null) {
                return "Unknown"
            } else {
                indicator_type = mapRequestIndicatorType.get(data);
                if (indicator_type) {
                    return indicator_type
                } else {
                    return "Unknown"
                }
            }
        }
    },
    {data: 'unit', 'sWidth': '10%', 'bSortable': false},
    {data: 'source_name', 'sWidth': '10%', 'bSortable': false},
    {data: 'order_no', 'sWidth': '10%', 'bSortable': true},
    {data: 'description', 'sWidth': '20%', 'bSortable': false},
    {
        data: 'approve_status', 'sWidth': '10%', 'bSortable': false,
        render: function (data, type) {
            if (data == null) {
                return "Unknown";
            } else {
                approve_status = mapApproveStatus.get(data);
                if (approve_status) {
                    return approve_status;
                } else {
                    return "Unknown";
                }
            }
        }
    },
    {data: 'reason', 'sWidth': '10%', 'bSortable': false},
    {data: 'edit_html', 'sWidth': '10%', 'bSortable': false}
];

var tb_options = {
    sAjaxDataProp: "data",
    iDisplayLength: 10,
    aLengthMenu: [10, 20, 50, 100],
    bServerSide: true,
    bDestroy: true,
    bInfo: true,
    bAutoWidth: false,
    stateSave: false,
    paging: true,
    bSort: false,//Cho ph�p s?p x?p
    bFilter: true,//S? d?ng b? l?c d? li?u(?n/hi?n thu?c t�nh t�m ki?m)
    sDom: "<'row middle't><'clear'><'row bottom' <'col-sm-6 text-left no-padding' li><'col-sm-6 text-right no-padding' p>><'clear'>",//�?nh nghia css cho c�c ph?n c?a b?ng
    bDeferRender: true,
    oLanguage: {
        "sZeroRecords": app.translate("JS_DT_NO_RECORD"),
        "sInfoEmpty": "",
        "sInfo": app.translate("JS_DT_DISPLAY") + " _START_ - _END_ (" + app.translate("JS_DT_IN") + " _TOTAL_)",
        "sInfoFiltered": "(Filter _MAX_ from results)",
        "sInfoPostFix": "",
        "sSearch": app.translate("JS_DT_SEARCH"),
        "sLengthMenu": "_MENU_",
        "sUrl": "",
        "oPaginate": {
            "sFirst": app.translate("JS_DT_FIRST"),
            "sPrevious": app.translate("JS_DT_PREVIOUS"),
            "sNext": app.translate("JS_DT_NEXT"),
            "sLast": app.translate("JS_DT_LAST")
        }
    }
};


$(document).ready(function () {
    loadDataTableForPage();
    $('#btn_search').click(function () {
        loadDataTableForPage()
    });
    $("#editModal").on("hide.bs.modal", function () {
        resetEditModalData();
    });
});

function alert(text, type) {
    toastr.options.positionClass = "toast-top-center";
    toastr.options.timeOut = 1500;
    console.log(type, text);
    toastr[type](text);
}

const requestIndicatorApproveStatusWaiting = 0
const requestIndicatorApproveStatusApproved = 1
const requestIndicatorApproveStatusRejected = 2


const mapApproveStatus = new Map([
    [requestIndicatorApproveStatusWaiting, "Chờ phê duyệt"],
    [requestIndicatorApproveStatusApproved, "Đã phê duyệt"],
    [requestIndicatorApproveStatusRejected, "Không phê duyệt"]
]);

const requestIndicatorTypeNT = 0
const requestIndicatorTypeNM = 1
const requestIndicatorTypeKK = 4
const requestIndicatorTypeKT = 3
const requestIndicatorTypeNN = 2

const mapRequestIndicatorType = new Map([
    [requestIndicatorTypeNT, "Nước thải (NT)"],
    [requestIndicatorTypeNM, "Nước mặt (NM)"],
    [requestIndicatorTypeKK, "Không khí (KK)"],
    [requestIndicatorTypeKT, "Khí thải (KT)"],
    [requestIndicatorTypeKT, "Khí thải (KT)"],
    [requestIndicatorTypeNN, "Nước ngầm (NN)"],

])


function loadDataTableForPage() {
    $table = $('#custom_datatable_0')
    var options = $.extend(tb_options, {
        bOrder: [[3, "desc"]],
        sAjaxSource: $table.attr('data-url'),
        fnServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "type", "value": $('#type').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "approve_status", "value": $('#approve_status').val()
            });
            $('#custom_datatable_0 tbody').empty()
            $.post(sSource, aoData, function (data) {
                fnCallback(data);
            })

        },
        "ajax": {
            "dataSrc": function (json) {
                for (var i = 0, ien = json.data.length; i < ien; i++) {
                    json.data[i].id_int = i + 1;
                    if (json.data[i].approve_status === requestIndicatorApproveStatusWaiting) {
                        var row = json.data[i]
                        json.data[i]['edit_html'] = `<a href=\"#\"><i class=\"fa fa-edit\" onclick=\"showEditModal('${row.id}')\"></i></a>\n`;
                    } else {
                        json.data[i]['edit_html'] = "";
                    }
                }
                return json.data
            }
        },
        columns: cols
    })
    $table.DataTable().clear().destroy();
    iTable = $table.dataTable(options)
}

function showEditModal(id) {
    $('#editModal').modal('toggle');
    $('#editModal').attr('data-id', id);
    setModaLoading();
    url = $('#hfUrlLinkGetRequestIndicator').val() + "/" + id
    app.postAjax(
        {
            url: url,
            handleResponse: function (data) {
                app.hideProgress();
                if (data.meta.code !== 200) {
                    app.showError(data.meta.message);
                    return true;
                }
            },
            callback: function (res) {
                if (res.meta.code === 200) {
                    setDataToEditModal(res.data);
                    setModaLoaded();
                }
            }
        }
    );
    // loading block
    // $('#approveModal').attr("data_id", );
}

function setDataToEditModal(data) {
    $('#update_indicator_name').val(data.indicator);
    $('#update_source_name').val(data.source_name);
    $("#update_indicator_type").val(data.indicator_type);
    $('#update_unit').val(data.unit);
    $('#update_order_no').val(data.order_no);
    $('#update_description').val(data.description);
}

// TODO set loading and disable button submit on that
function setModaLoading() {
    $('#editModalTitle').text('Đang tải')
    $('#editModal').attr("disabled", true);
}

function setModaLoaded() {
    $('#editModalTitle').text('Cập nhật yêu cầu tạo thông số');
    $('#editModal').removeAttr("disabled");
}


function submitSave() {
    var riID = $('#editModal').attr('data-id');
    if (riID) {
        updateRequestIndicator(riID);
    } else {
        createRequestIndicator();
    }
}

function createRequestIndicator() {
    var indicatorName = $('#update_indicator_name').val();
    var sourceName = $('#update_source_name').val();
    var indicatorTypeStr = $("#update_indicator_type").val();
    var indicatorType = parseInt(indicatorTypeStr, 10);
    var unit = $('#update_unit').val();
    var orderNoStr = $('#update_order_no').val();
    var orderNo = parseInt(orderNoStr, 10);
    var description = $('#update_description').val();
    url = $('#hfUrlLinkCreateRequestIndicator').val();
    app.postAjax(
        {
            url: url,
            contentType: "application/json; charset=utf-8",
            enctype: null,
            data: JSON.stringify({
                indicator: indicatorName,
                source_name: sourceName,
                indicator_type: indicatorType,
                unit: unit,
                description: description,
                order_no: orderNo
            }),
            handleResponse: function (data) {
                app.hideProgress();
                if (data.meta.code !== 200) {
                    app.showError(data.meta.message);
                    return true;
                }
            },
            callback: function (res) {
                if (res.meta.code === 200) {
                    $('#editModal').modal('hide');
                    loadDataTableForPage();
                }
            }
        }
    );
}

function updateRequestIndicator(requestIndicatorID) {
    var indicatorName = $('#update_indicator_name').val();
    var sourceName = $('#update_source_name').val();
    var indicatorTypeStr = $("#update_indicator_type").val();
    var indicatorType = parseInt(indicatorTypeStr, 10);
    var unit = $('#update_unit').val();
    var orderNo = $('#update_order_no').val();
    var description = $('#update_description').val();
    url = $('#hfUrlLinkUpdateRequestIndicator').val() + "/" + requestIndicatorID;
    app.postAjax(
        {
            url: url,
            contentType: "application/json; charset=utf-8",
            enctype: null,
            data: JSON.stringify({
                indicator: indicatorName,
                source_name: sourceName,
                indicator_type: indicatorType,
                unit: unit,
                description: description,
                order_no: orderNo
            }),
            handleResponse: function (data) {
                app.hideProgress();
                if (data.meta.code !== 200) {
                    app.showError(data.meta.message);
                    return true;
                }
            },
            callback: function (res) {
                if (res.meta.code === 200) {
                    $('#editModal').modal('hide');
                    loadDataTableForPage();
                }
            }
        }
    );
}

function resetEditModalData() {
    $('#editModal').attr('data-id', '');
    $('#update_indicator_name').val('');
    $('#update_source_name').val('');
    $('#update_indicator_type').val('0');
    $('#update_unit').val('');
    $('#update_order_no').val('');
    $('#update_description').val('');
}



