$(document).ready(function() {
    loadDataTableForPage();
    
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});

function reloadDatatable_Equipment() {
    oTable[0].fnFilter('');
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%'},
        {'sWidth' : '20%'},
        {'sWidth' : '17%'},
        {'sWidth' : '10%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},
    ];

    var aoClass = ['', 'text-left', '', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "station_id", "value": $('#station_id').val()
            });
            aoData.push({
                "name": "status", "value": $('#status').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
        },
    });
    
    return true;
}

