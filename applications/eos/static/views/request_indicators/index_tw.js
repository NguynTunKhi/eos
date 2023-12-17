$(document).ready(function () {
    loadDataTableForPage();
    $('#btn_search').click(function () {
        oTable[0].fnFilter('');
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

const requestIndicatorApproveStatusWaiting = 0
const requestIndicatorApproveStatusApproved = 1
const requestIndicatorApproveStatusRejected = 2


const mapApproveStatus = new Map([
    [requestIndicatorApproveStatusWaiting, "Chờ phê duyệt"],
    [requestIndicatorApproveStatusApproved, "Đã phê duyệt"],
    [requestIndicatorApproveStatusRejected, "Không phê duyệt"]
]);

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var length_column = $('#tr-table>th').length;

    var aoColumns = [
        {'sWidth': '5%', 'bSortable': false},
        {'sWidth': '5%'},
        {'sWidth': '5%'},
        {'sWidth': '5%'},
        {'sWidth': '5%'},
        {'sWidth': '5%'},
        {'sWidth': '10%'},
        {'sWidth': '5%'},
        {'sWidth': '10%'},
        {'sWidth': '5%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', '', '', 'text-center', 'text-right', ''];
    // var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,

        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "type", "value": $('#type').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "approve_status", "value": $('#approve_status').val()
            });
        },
        fnCustomCallback: function (data) {
            data.aaData.forEach(function (value, index, array) {
                if (value[7] != null) {
                    value[7] = mapApproveStatus.get(value[7]);
                }
            })
        }
    });

    return true;
}

function showApproveModal(requestIndicatorID) {
    $('#approveModal').modal('toggle');
    $('#approveModal').attr("data-id", requestIndicatorID);
}

function resetModalData() {
    $('#approveModal').attr('data-id', '');
    $('#reason').val('');
}

function submitApprove() {
    var approve_action = $('#riSelectAction').find(":selected").val();
    var reason = $('#reason').val();
    var requestIndicatorID = $('#approveModal').attr('data-id');
    url = $('#hfUrlLinkApproveIndicator').val()
    app.postAjax(
        {
            url: url,
            data: {
                request_indicator_id: requestIndicatorID,
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
                    oTable[0].fnDraw();
                    $('#approveModal').modal('hide');
                }
            }
        }
    );
}

function resetApproveModalData() {
    $('#approveModal').attr('data-id', '');
    $('#riSelectAction').val('0');
    $('#reason').val('');
}



