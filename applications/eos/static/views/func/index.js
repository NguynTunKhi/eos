$(document).ready(function() {
    loadDataTableForPage();
    // var loadtable = false;
    // var search = false;
    
    // $('#btn_search').click(function(){
        // if (loadtable == false) {
            // loadtable = loadDataTableForPage();
        // }
        // if (search == true) {
            // oTable[0].fnFilter('');
        // }
        // search = true;
    // });
    
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '25%'},
        {'sWidth' : '40%'},
        {'sWidth' : '25%'},
        {'sWidth' : '5%'},   // For check box column
    ];

    var aoClass = ['', '', 'text-left', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
    
    return true;
}