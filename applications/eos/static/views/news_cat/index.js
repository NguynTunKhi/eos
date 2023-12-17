/**
 * Created by Admin on 8/8/2017.
 */

$(document).ready(function() {
    loadDataTableForPage();
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        { "sWidth": "5%", "bSortable": false },
        { "sWidth": "75%" },
        { "sWidth": "15%" },
        { "sWidth": "5%", "bSortable": false }
    ];

    var aoClass = ['', 'text-left', 'text-left', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
}

function reloadDatatable() {
    oTable[0].fnDraw();
}