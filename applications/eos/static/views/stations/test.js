$(document).ready(function() {
    loadDataTableForPage();
    
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});

function loadDataTableForPage() {
    // Remove all addition fields
    var aoColumns = [
        {'sWidth' : '2%', 'bSortable' : false},
        {'sWidth' : '3%', 'bSortable' : false},
        {'sWidth' : '12%'},
        {'sWidth' : '12%'},
    ];

    var aoClass = ['', '', 'text-left', 'text-left'];
    loadDataTable({
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
    
    return true;
}