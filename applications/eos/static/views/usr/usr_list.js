/**
 * Created by Admin on 8/8/2017.
 */

$(document).ready(function() {
    loadDataTableForPage();
});

function loadDataTableForPage() {
    if (typeof loadDataTable == "function"){
        var sAjaxSource = $("#custom_datatable_0").attr("data-url");
        var aoColumns = [
                        { "sWidth": "5%", "bSortable": false },
                        { "sWidth": "25%" },
                        { "sWidth": "25%" },
                        { "sWidth": "40%" },
                        { "sWidth": "5%", "bSortable": false }
                        ];

        var aoClass = ['', 'text-left', 'text-left', 'text-left'];
        loadDataTable({
            sAjaxSource: sAjaxSource,
            aoColumns: aoColumns,
            aoClass: aoClass,
        });
    } else {
        setTimeout(loadDataTableForPage, 30);
    }
}