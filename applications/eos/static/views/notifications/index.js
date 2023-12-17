/**
 * Created by Admin on 8/8/2017.
 */

$(document).ready(function() {
    loadDataTableForPage();
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
                    {'sWidth' : '4%', 'bSortable' : false},
                    {'sWidth' : '35%'},
                    {'sWidth' : '39%'},
                    {'sWidth' : '12%'},
                    {'sWidth' : '10%'},
                    ];

    var aoClass = ['', 'text-left', 'text-left', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
}