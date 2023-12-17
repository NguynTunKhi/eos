var cols = [
    {data: 'station_name', 'sWidth': '10%', 'bSortable': false},
    {data: 'str_station_type', 'sWidth': '10%', 'bSortable': false},
    {data: 'email', 'sWidth': '10%', 'bSortable': false},
    {data: 'phone', 'sWidth': '10%', 'bSortable': false},
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
    {data: 'station_link', 'sWidth': '10%', 'bSortable': false},
    {data: 'reason', 'sWidth': '10%', 'bSortable': false},
    {data: 'form_detail_html', 'sWidth': '5%', 'bSortable': false},
    {data: 'approve_html', 'sWidth': '5%', 'bSortable': false}
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
    $("#approveModal").on("hide.bs.modal", function () {
        resetApproveModalData();
    });
});

function alert(text, type) {
    toastr.options.positionClass = "toast-top-center";
    toastr.options.timeOut = 1500;
    console.log(type, text);
    toastr[type](text);
}

const requestSyncStationApproveStatusWaiting = 0
const requestSyncStationApproveStatusApproved = 1
const requestSyncStationApproveStatusRejected = 2


const mapApproveStatus = new Map([
    [requestSyncStationApproveStatusWaiting, "Chờ phê duyệt"],
    [requestSyncStationApproveStatusApproved, "Đã phê duyệt"],
    [requestSyncStationApproveStatusRejected, "Không phê duyệt"]
]);


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
                    if (json.data[i].approve_status === requestSyncStationApproveStatusWaiting) {
                        var row = json.data[i]
                        json.data[i]['approve_html'] = `<a href=\"#\"><i class=\"fa fa-edit\" onclick=\"showApproveModal('${row.id}')\"></i></a>\n`;
                    } else {
                        json.data[i]['approve_html'] = "";
                    }
                    if (json.data[i].station_id_decimal) {
                        href = window.location.origin + "/eos/stations/form/" + json.data[i].station_id_decimal + "?preview=true";
                        json.data[i]['station_link'] = `<a href="${href}"><i>${json.data[i].station_name}</i></a>\n`
                    } else {
                        json.data[i]['station_link'] = "";
                    }
                    if (json.data[i].request_sync_station_id) {
                        hrefx = window.location.origin + "/eos/request_sync_stations/form/" + json.data[i].request_sync_station_id;
                        json.data[i]['form_detail_html'] = `<a href="${hrefx}"><i class=\"fa fa-edit\"></i></a>`;
                    } else {
                        json.data[i]['form_detail_html'] = "";
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

function showApproveModal(rssID) {
    $('#approveModal').modal('toggle');
    $('#approveModal').attr("data-id", rssID);
}

function submitApprove() {
    var approve_action = $('#rssSelectAction').find(":selected").val();
    var reason = $('#reason').val();
    var requestSyncStationID = $('#approveModal').attr('data-id');
    url = $('#hfUrlLinkApproveRequestSyncStation').val()
    app.postAjax(
        {
            url: url,
            data: {
                request_sync_station_id: requestSyncStationID,
                approve_action: approve_action,
                reason: reason,
            },
            handleResponse: function (data) {
                app.hideProgress();
                if (data.meta.code !== 200) {
                    app.showError(data.meta.message);
                    return true;
                }
            },
            callback: function (res) {
                if (res.meta.code === 200) {
                    $('#approveModal').modal('hide');
                    loadDataTableForPage()
                }
            }
        }
    );
}

function resetApproveModalData() {
    $('#approveModal').attr('data-id', '');
    $('#rssSelectAction').val('0');
    $('#reason').val('');
}



