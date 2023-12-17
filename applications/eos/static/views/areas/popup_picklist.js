/**
 * Created by Admin on 8/3/2017.
 */

$(document).ready(function() {
    loadDataTableForCustomerPopupPicklist();
    
    $('.dataTables_wrapper').css("padding-bottom", 0);
    $('#custom_datatable_station_popup_picklist_length').addClass("hide");
});

function loadDataTableForCustomerPopupPicklist() {
    if (typeof loadDataTable == "function"){
        var iTable = "customers_popup_picklist";
        var table = $("table#custom_datatable_" + iTable).attr("data-table");
        var field = $("table#custom_datatable_" + iTable).attr("data-field");
        var extend = $("table#custom_datatable_" + iTable).attr("data-extend");
        var url = $("table#custom_datatable_" + iTable).attr("data-url");
        var aoColumns = [
                            { 'sWidth': '3%', 'bSortable': false },
                            { 'sWidth': '20%' },
                            { 'sWidth': '55%' },
                            { 'sWidth': '20%' },
                            { 'sWidth': '2%' }
                        ];

        var aoClass = ['', 'text-left', 'text-left', '', ''];
        // var sDom = "<'middle't><'clear'><'row bottom' <'col-sm-6 text-left' ><'col-sm-6 text-right' p>><'clear'>";
        loadDataTable({
            sAjaxSource: url,
            aoColumns: aoColumns,
            aoClass: aoClass,
			iDisplayLength: "5",
            iTable: iTable,
            // sDom: sDom,
        });
        
        $('.dataTables_wrapper').css("padding-bottom", 0);
        $('#custom_datatable_station_popup_picklist_length').addClass('hide');
    } else {
        setTimeout(loadDataTableForCustomerPopupPicklist, 30);
    }

}