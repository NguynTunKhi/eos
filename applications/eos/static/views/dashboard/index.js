

$(document).ready(function() {
    app.registerEventsForCommonInput();
    
    $('.indicator .ibox-content').click(function() {
        window.location.href = "/eos/log_min/index";
    });
    
    $('.progress .progress-bar').css("width",
        function() {
            return $(this).attr("aria-valuenow") + "%";
        }
    );
    
    $('.scroll_content').slimscroll({
        height: '700px'
    });

    $('body').on('change', '#block2_province_id, #block2_area_id', function (e) {
        loadContentForBlock2();
    });
    
    // Height of scroll_content_aqi
    $('.scroll_content_aqi').slimscroll({
        height: '350px'
    });
    
    $('.scroll_content_inactive').slimscroll({
        height: '360px'
    });
    
    $('.scroll_content_notify').slimscroll({
        height: '375px'
    });
    // Block 3

    $('body').on('click', '.btnGlobalGo', async function (e) {
        var params = {
            area_id: $('#global_area_id').val(),
            province_id: $('#global_province_id').val(),
        };
        // Block 1 cu
        // reloadSummaryStation();

        // For widget_by_station_type
        var table_wbst = $('[id*="wbst-tab-"]');
        var total_tab = table_wbst.length;
        for (var i=0; i<total_tab; i++){
            var idx = $(table_wbst[i]).attr('id').replace('wbst-tab-', '');
            oTable['wbst_' + idx].fnFilter('');
        }

        // AQI block
        oTable['aw'].fnFilter('');
        
        // Data collect block
        loadDataForDataCollect();
        // Station distribution
        var station_distribution = '';
        // if ($('#global_province_id').val() != '' || $('#global_area_id').val() != '') {
            station_distribution = $('#widget_station_distribution_div').data('url') + '?' + $.param(params);
            $('#widget_station_distribution_div').load(station_distribution);
        // }
        
        // Block 1 : station type
        var station_type = $('#station_type_div').data('url') + '?' + $.param(params);
        var data = await  fetch(station_type)
        await $("#station_type_div").html(await data.text());

        var block2interval = setInterval(function (e) {
            var condition_status_url = $('#blockChart2').data('url');
            if (condition_status_url == "") {
                return false;
            }
            clearInterval(block2interval);
            $('#blockChart2').load(condition_status_url + '?' + $.param(params));
        })
        // Condition status block

    });

    loadContentForBlock2();
    loadDataForDataCollect();
});

function loadDataForDataCollect() {
        var params = {
            area_id: $('#global_area_id').val(),
            province_id: $('#global_province_id').val(),
        };
        var widget_collect_url = $('#widget_data_collect_div').data('url');
        $('#widget_data_collect_div').load(widget_collect_url + '?' + $.param(params));
}

function reloadSummaryStation() {
    var params = {
        area_id: $('#global_area_id').val(),
        province_id: $('#global_province_id').val(),
    };
    var url = $('#hfURLGetDataForSummaryStation').val();
    app.postAjax({
        url: url,
        showProgress: false,
        data: params,
        callback: function (res) {
            if (res.success){
                $('.summary_station_online').html(res.total_online.toString() + '/' + res.total_station.toLocaleString());
                var station_type_online = res.station_type_online;
                for(var key in station_type_online) {
                    var sto = station_type_online[key];
                    $('.summary-station-' + sto.value.toString()).html(sto.online.toString() + '/' + sto.total.toLocaleString());
                }
            }
        }
    });
}

function loadContentForBlock2() {
    var url = $('#blockChart2').data('url');
    url += "?";
    var params = {
        province_id: $('#block2_province_id').val(),
        area_id: $('#block2_area_id').val(),
    };
    url += $.param(params);
    app.showProgress('#blockChart2');
    $('#blockChart2').load(url, function (e) {
        app.hideProgress('#blockChart2');
    });
}