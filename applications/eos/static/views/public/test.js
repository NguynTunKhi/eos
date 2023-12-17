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
    ];

    var aoClass = ['', 'text-left', '', '', 'text-left', 'text-left', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        
    });
    
    return true;
}

// function reloadDatatable_alarm_logs() {
    // oTable[0].fnDraw();
// }