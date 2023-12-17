
$(document).ready(function () {
    var recordId = $('#hfRequestCreateStationId').val();
    if (recordId) {
        loadStationProfileDataTableForPage();
        loadStationProfileDataTable_Indicator();
        loadStationProfileDataTable_camera();
        loadStationProfileDataTable_auto_adjust();
        loadStationProfileDataTable_DataCommand();
    }
});

function loadStationProfileDataTable_Indicator() {
    var sAjaxSource = $("#custom_datatable_indicator").attr("data-url");
    var aoColumns = [
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '16%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', 'text-right', '', ''];
    var sDom = "<'row middle horizontal-scroll't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "request_create_station_id", "value": $('#hfRequestCreateStationId').val(),
            });
            aoData.push({
                "name": "view_only", "value": true,
            });
        },
        iTable: "indicator"
    });

    return true;
}

function loadStationProfileDataTable_camera() {
    var sAjaxSource = $("#custom_datatable_camera").attr("data-url");
    var aoColumns = [
        {'sWidth': '5%'},
        {'sWidth': '10%'},
        {'sWidth': '20%'},
        {'sWidth': '45%'},
        {'sWidth': '5%'},
    ];

    var aoClass = ['', '', 'text-left', 'text-left', '', '', '', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        iTable: "camera",
    });

    return true;
}

function loadStationProfileDataTable_auto_adjust() {
    var sAjaxSource = $("#custom_datatable_auto_adjust").attr("data-url");
    var aoColumns = [
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '20%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '20%'},
    ];

    var aoClass = ['', '', '', '', '', '', '',''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "request_create_station_id", "value": $('#hfRequestCreateStationId').val(),
            });
            aoData.push({
                "name": "view_only", "value": true,
            });
        },
        iTable: "auto_adjust"
    });

    return true;
}

function loadStationProfileDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_equipment").attr("data-url");
    var aoColumns = [
        {'sWidth': '3%'},
        {'sWidth': '25%'},
        {'sWidth': '10%'},
        {'sWidth': '15%'},
        {'sWidth': '13%'},
        {'sWidth': '10%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
        {'sWidth': '8%'},
    ];

    var aoClass = ['', 'text-left', '', 'text-left', 'text-left', '', 'text-right', 'text-right', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        iTable: "equipment"
    });

    return true;
}

function loadStationProfileDataTable_DataCommand() {
    var sAjaxSource = $("#custom_datatable_datalogger").attr("data-url");
    var cols = ['Command content', 'Username', 'IP', 'Command title'];
        aoColumns = [
            {'sWidth': '3%', 'bSortable': false},
            {'sWidth': '35%'},
            {'sWidth': '24%'},
            {'sWidth': '22%'},
            {'sWidth': '22%'}
        ];
    var aoClass = ['', 'text-left', '', '', '', ''];
    for (var inx = 0; inx < cols.length; inx++) {
        $("<th>" + app.translate(cols[inx]) +"</th>").insertAfter('#r-no');
    }

    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        iTable: "datalogger"
    });

    return true;
}