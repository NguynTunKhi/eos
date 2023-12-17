$(document).ready(function() {
    loadDataTableForPage();
        
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
    
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%'},
        {'sWidth' : '15%'},
        {'sWidth' : '60%'},
        {'sWidth' : '15%'},
        {'sWidth' : '5%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', '', '', '', '', '', ''];
    // var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        // sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "station_id", "value": $('#station_id').val()
            });
            aoData.push({
                "name": "command_id", "value": $('#command_id').val()
            });
            aoData.push({
                "name": "from_date", "value": $('#from_date').val()
            });
            aoData.push({
                "name": "to_date", "value": $('#to_date').val()
            });
        },
    });
    
    return true;
}

