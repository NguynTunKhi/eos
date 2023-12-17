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
        { "sWidth": "15%" },
        { "sWidth": "25%" },
        { "sWidth": "20%" },
        { "sWidth": "15%" },
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