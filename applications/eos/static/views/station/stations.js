$(document).ready(function(){

    loadDataTableForPage();
    
    // Height of list stations
    $('.scroll_content').slimscroll({
        height: '450px'
    })
    
    // Select station on left list --> display detail info on the right panel
    $('body').on('click', '#custom_datatable_0 tbody tr' , function(e){
        if ($(this).hasClass('selected')){
            // Click vao row dang dc select --> ko lam gi ca
        } else {
            $(this).closest('tbody').find('tr').removeClass('selected');
            $(this).addClass('selected');
            var id = $(this).data('id');
            $('#hfStationId').val(id);

            // Call action to redraw right panel
            var stationId = $('#hfStationId').val();
            var show_by = $('#cbbShowBy').val();
            var url = $('#hfUrlLoadGraph').val();
            
            url += "?" + $.param({station_id: stationId, show_by: show_by});
            $("#graph_detail").load(url);
            
            // Hide button "Adjust data"
            // $('#adjust_data').addClass('hide');
            $('.graph_detail_adjust_data').addClass('hide');
        }
    });
    
    // Filter station by province
    $("#province_id").change(function () {
        loadDataTableForPage();
        
        filter_station('province_id', $("#province_id").val());
    });
    
    $("#area_id").change(function () {
        loadDataTableForPage();
        
        filter_station('area_id', $("#area_id").val());
    });
    
    $("#station_id").change(function () {
        loadDataTableForPage();
    });
    
    var $report = $('#report');
});

// Filter station
function filter_station(filter_field, filter_value) {
    var url = "/eos/stations/call/json/dropdown_content/stations/" + filter_field + "/id/station_name";
    app.postAjax({
        url: url,
        data: {filter_value : filter_value},
        
        callback: function (res) {
            if (res.success) {
                $('#station_id').html(res.html);
                $('#station_id').trigger("chosen:updated");
            } else {
                app.showError(res.message);
            }
        }
    });
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var province_id = $("#province_id").val();
    var area_id = $("#area_id").val();
    var station_id = $("#station_id").val();
    
    if (province_id != '') sAjaxSource += '&province_id=' + province_id;
    if (area_id != '') sAjaxSource += '&area_id=' + area_id;
    if (station_id != '') sAjaxSource += '&station_id=' + station_id;
    
    var aoColumns = [
        // { "sWidth": "5%", "bSortable": false },
        { "sWidth": "75%" },
        { "sWidth": "25%" },
        ];
    var sDom = "<'row middle't><'clear'>";
    var aoClass = ['text-left', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomDrawCallback: function () {
            $( "tbody tr" ).first().trigger('click');
        }
    });
    
    // chinh CSS cua table list station
    var wrap = $('#custom_datatable_0').closest('.middle');
    wrap.removeClass('row');
}

function reloadDetailTab() {
    
}