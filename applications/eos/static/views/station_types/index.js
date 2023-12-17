$(document).ready(function() {
    loadDataTableForPage();
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '10%', 'bSortable' : false},
        {'sWidth' : '20%'},
        {'sWidth' : '15%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},   // For check box column
    ];

    var aoClass = ['', '', 'text-left', '', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
    });
    
    return true;
}

