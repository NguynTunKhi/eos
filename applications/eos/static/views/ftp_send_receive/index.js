$(document).ready(function() {
    loadDataTableForPage();
    
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%'},
        {'sWidth' : '22%'},
        {'sWidth' : '22%'},
        {'sWidth' : '20%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '3%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', 'text-left', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "from_date", "value": $('#from_date').val()
            });
            aoData.push({
                "name": "to_date", "value": $('#to_date').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
        },
    });
    
    return true;
}

