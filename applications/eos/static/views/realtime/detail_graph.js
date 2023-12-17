$(document).ready(function(){
    // Khi view mode thay doi ngay start display
    $('body').on('click', '#btn_go' , function(e){
        var indicatorId = $('#hfIndicator').val();
        if (indicatorId == 'all') {
            createChartForStationForAll();
        } else {
            createChartForStationForItem(indicatorId);
        }
    });
    
    $('body').on('click', '#btnRefresh' , function(e){
        $('#chartStart').val('');
        $('#btn_go').trigger('click');
    });
    
    setInterval(function() {
        $('#btnRefresh').trigger('click');
    }, 300*1000);

});

function loadGraphicForStation() {
    var stationId = $('#cbbStationId').val();
    if (stationId) {
        var show_by = $('#hfViewType').val();
        var url = $('#hfUrlLoadGraph').val();

        // 2 bien Start / From duoc lay o 'load_import/graph_detail.js

        url += "?" + $.param({station_id: stationId, show_by: show_by});
        $("#graph_detail").load(url);

        // Display adjust data button
        $('#adjust_data').removeClass('hide');
    } else {
        $("#graph_detail").html(app.translate('No data found!'));
    }
}