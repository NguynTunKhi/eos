/**
 * Created by Admin on 8/3/2017.
 */

$(document).ready(function() {
    loadDataTableForStationPopupPicklist();

    $('body').on('click' , '#btnSearchStationOnPopup' , function(e){
       oTable['station_popup_picklist'].fnDraw();
    });

    $('body').off('change', '#cbbStationType');
    $('body').on('change', '#cbbStationType', function (e) {
        $('#hfStationType').val($(this).val());
    });
    $('#cbbStationType').trigger('change');
});

function loadDataTableForStationPopupPicklist() {
    if (typeof loadDataTable == "function"){
        var iTable = "station_popup_picklist";
        var table = $("table#custom_datatable_" + iTable).attr("data-table");
        var field = $("table#custom_datatable_" + iTable).attr("data-field");
        var extend = $("table#custom_datatable_" + iTable).attr("data-extend");
        var url = $("table#custom_datatable_" + iTable).attr("data-url");
        var aoColumns = [
                            { 'sWidth': '5%', 'bSortable': false },
                            { 'sWidth': '30%' },
                            { 'sWidth': '60%' },
                            { 'sWidth': '5%' },
                        ];

        var aoClass = ['', 'text-left', 'text-left', '', ''];
        loadDataTable({
            sAjaxSource: url,
            aoColumns: aoColumns,
            aoClass: aoClass,
			iDisplayLength: "5",
            sDom: "<'row middle't><'clear'><'row bottom' <'col-sm-6 text-left' i><'col-sm-6 text-right' p>><'clear'>",
            iTable: iTable,
            fnCustomServerData: function (sSource, aoData, fnCallback) {
                aoData.push({
                    "name": "station_type", "value": $('#cbbStationType').val(),
                    "name": "province_id", "value": $('#cbbProvinceId').val()
                });
                aoData.push({
                    "name": "sSearch2", "value": $('#txtSearchStationOnPopup').val()
                });
            },
        });
    } else {
        setTimeout(loadDataTableForStationPopupPicklist, 30);
    }

}