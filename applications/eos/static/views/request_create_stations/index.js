$(document).ready(function() {
    loadDataTableForPage();
    $("#approveModal").on("hide.bs.modal", function () {
        resetApproveModalData();
    });
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });



});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '2%', 'bSortable' : true},
        {'sWidth' : '4%'},
        {'sWidth' : '5%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '10%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '2%'},
        {'sWidth' : '5%'},
        {'sWidth' : '5%'},
        {'sWidth' : '18%'},
        {'sWidth' : '3%'},
        {'sWidth' : '3%'},
        {'sWidth' : '3%'},
    ];

    var aoClass = ['', 'text-left td-station-name', '', '', 'text-left', 'text-left','', '', '', ''];
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
                "name": "province_id", "value": $('#province_id').val()
            });
            aoData.push({
                "name": "status", "value": $('#status').val()
            });
            aoData.push({
                "name": "ftp_connection_status", "value": $('#ftp_connection_status').val()
            });
            aoData.push({
                "name": "approve_status", "value": $('#approve_status').val()
            });
        },

    });

    return true;
}

function sortRequestCreateStation(n){
        var x = document.getElementById("sorts")
        if (x.getAttribute('sort') === 'True'){
            document.getElementById("sorts").setAttribute('sort', 'False');
            var sort_type = 0
        }
        else {
            document.getElementById("sorts").setAttribute('sort', 'True');
            var sort_type = 1
        }

        var sAjaxSource = $("#custom_datatable_0").attr("data-url")+"_sort";
        var aoColumns = [
        {'sWidth' : '2%', 'bSortable' : true},
        {'sWidth' : '4%'},
        {'sWidth' : '5%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '10%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '8%'},
        {'sWidth' : '2%'},
        {'sWidth' : '5%'},
        {'sWidth' : '5%'},
        {'sWidth' : '18%'},
        {'sWidth' : '3%'},
        {'sWidth' : '3%'},
        {'sWidth' : '3%'},
    ];

    var aoClass = ['', 'text-left td-station-name', '', '', 'text-left', 'text-left','', '', '', ''];
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
                "name": "province_id", "value": $('#province_id').val()
            });
            aoData.push({
                "name": "status", "value": $('#status').val()
            });
            aoData.push({
                "name": "ftp_connection_status", "value": $('#ftp_connection_status').val()
            });
            aoData.push({
                "name": "sort_type", "value": sort_type
            });
            aoData.push({
                "approve_status": "approve_status", "value": $('#approve_status').val()
            });
        },

    });

    return true;
}


function showApproveModal(requestCreateStationID) {
    $('#approveModal').modal('toggle');
    $('#approveModal').attr("data-id", requestCreateStationID);
}

function resetApproveModalData() {
    $('#approveModal').attr('data-id', '');
    $('#rcsSelectAction').val('0');
    $('#reason').val('');
}

function resetModalData() {
    $('#approveModal').attr('data-id', '');
    $('#reason').val('');
}

function submitApprove() {
    var approve_action = $('#rcsSelectAction').find(":selected").val();
    var reason = $('#reason').val();
    var requestCreateStationID = $('#approveModal').attr('data-id');
    url = $('#hfUrlLinkApproveRequestCreateStation').val()
    app.postAjax(
        {
            url: url,
            data: {
                request_create_station_id: requestCreateStationID,
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