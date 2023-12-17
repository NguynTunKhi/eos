$(document).ready(function() {
    loadDataTableForPage();

    // $('#btn_search').click(function(){
        // oTable[0].fnFilter('');
    // });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '2%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
    ];

    var aoClass = ['', 'text-left', '', '', 'text-left', 'text-left', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        // fnCustomServerData: function (sSource, aoData, fnCallback) {
            // aoData.push({
                // "name": "from_date", "value": $('#from_date').val()
            // });
            // aoData.push({
                // "name": "to_date", "value": $('#to_date').val()
            // });
            // aoData.push({
                // "name": "sometext", "value": $('#sometext').val()
            // });
        // },
    });

    return true;
}

// function reloadDatatable_alarm_logs() {
    // oTable[0].fnDraw();
// }