var url = 'http://api.openweathermap.org/data/2.5/weather?lat=21.026502&lon=105.848380&appid=b3c6503ac31cb5e72765e98cd0d7795e&units=metric&lang=vi&cnt=64';
 var siteUrl = '/eos'; // Khong co dau / o cuoi url
// var siteUrl = 'http://enviinfo.cem.gov.vn/eos';
var map = null;
var json_station_status = null;
var json_indicators = null;
var json_stations = null;
var json_area = null;
var json_provinces = null;
var indexItems = [
    {
        from: 0,
        to: 50,
        text: '0 - 50',
        name: 'Tốt',
        bg: '#319967',
        color: '#fff',
    },
    {
        from: 51,
        to: 100,
        text: '51 - 100',
        name: 'Trung bình',
        bg: '#fee05b',
        color: '#666',
    },
    {
        from: 101,
        to: 150,
        text: '101 - 150',
        name: 'Kém',
        bg: '#fe9b4c',
        color: '#fff',
    },
    {
        from: 151,
        to: 200,
        text: '151 - 200',
        name: 'Xấu',
        bg: '#cc3635',
        color: '#fff',
    },
    {
        from: 201,
        to: 300,
        text: '201 - 300',
        name: 'Nguy hại',
        bg: '#6a499a',
        color: '#fff',
    },
    {
        from: 301,
        text: 'Trên 300',
        name: 'Rất nguy hại',
        bg: '#7f1f25',
        color: '#fff',
    },
];

$(document).ready(function(){
    json_station_status = $('#json_station_status').html();
    json_station_status = JSON.parse(json_station_status);
    indexItems = $('#json_index_items').html();
    indexWQIItems = $('#json_index_items_wqi').html();
    indexItems = JSON.parse(indexItems);
    json_indexWQIItems = JSON.parse(indexWQIItems);
    json_indicators = $('#json_indicators').html();
    json_indicators = JSON.parse(json_indicators);
    json_stations = $('#json_stations').html();
    json_stations = JSON.parse(json_stations);
    json_area = $('#json_area').html();
    json_area = JSON.parse(json_area);
    json_provinces = $('#json_provinces').html();
    json_provinces = JSON.parse(json_provinces);
    var addCustomFuncitonToMapInterval = setInterval(function () {
        var panelTieuChuan = $("#map>div").find(".panelTieuChuan");
        if (panelTieuChuan.length != 0) {
            clearInterval(addCustomFuncitonToMapInterval);
        } else {
            var html = "<div class='panelTieuChuan'>";
            for (var key in indexItems) {
                html += "<div  title='" + indexItems[key].text + "' style='background-color: " +
                    indexItems[key].bgColor + "; color: " + indexItems[key].color + ";'><i>";
                if (indexItems[key]['to']){
                    html += indexItems[key]['from'] + ' - ' + indexItems[key]['to'];
                } else {
                    html += 'Trên ' + indexItems[key]['from'];
                }
                html += ":</i>&nbsp;<span>" + indexItems[key].text + "</span></div>";
            }
            html += "</div>" +
                "<div class='panelControl'>" +
                 "<label><input class='chkShowHideLabel' type='checkbox'>" + app.translate('Show labels') + "</label>"
            html += "</div>" +
            "</div>";
            $("#map>div").append(html);

            showHideIndicatorsBar();
        }
    }, 300);

	var showClockOnMapInterval = setInterval(function(){
        var currentTime = new Date();
        var hours = currentTime.getHours();
        var minutes = currentTime.getMinutes();
        var seconds = currentTime.getSeconds();
        var displayTime = app.formatTime(hours, minutes, seconds);
		$(".panelControl>span").html(displayTime);
	}, 1000);

	$("body").on('click', '.toolParameters', function (e) {
	    $(this).find('.items').show();
    });

	$("body").on('click', '.closePopover', function (e) {
	    $(this).closest('.popover').closest('.ol-overlay-container').find(".mapMarker").trigger('click');
    });

	$("body").on('mouseleave', '.toolParameters .items', function (e) {
	    $(this).hide();
    });


	$('body').on('click', '.chkShowHideLabel', function (e) {
	    if ($(this).prop('checked')){
            // $('.mapLabel').show();
            $('.mapLabel[data-station_type="' + $('#cbbStationType').val() + '"]').show();
        } else {
	        $('.mapLabel').hide();
        }
    });

	$('body').on('click', '.toolParameters .item input', function (e) {
	    var id = $(this).closest('.item').data('id');
	    if ($(this).prop('checked')){
            $('.mapLabel').find('.param[data-id=' + id + ']').show();
        } else {
	        $('.mapLabel').find('.param[data-id=' + id + ']').hide();
        }
    });

	$('body').on('click', '.mapLabel h4', function (e) {
	    var parent =  $(this).closest('.mapLabel');
	    parent.find('p').hide();
	    var id = parent.data('id');
       $('.mapMarker[data-id=' + id + ']').trigger('click', [true]);
    });

	$('body').on('click', '#custom_datatable_3 a', function (e) {
	    var lat = $(this).data('lat');
	    var lon = $(this).data('lon');
	    map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
        var id = $(this).data('id');
        $('.mapMarker[data-id=' + id + ']').trigger('click', [true]);
    });

	$('body').on('change', '#cbbStations', function (e) {
	    var valueSelect = $("#cbbStations").val();
	    if (valueSelect == null || valueSelect == "") {
	         return false;
        }
	    var selectedOption = $(this).find('option:selected');
	    var lat = selectedOption.data('lat');
	    var lon = selectedOption.data('lon');
	    map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
        var id = selectedOption.data('id');
        // $('.mapMarker[data-id=' + id + ']').trigger('click', [true]);
        // Show chart on left bar
        var stationId  = $('#cbbStations').val();
        var stationType  = $('#cbbStationType').val();
        // var address = $(this).attr("data-address");
        var province = selectedOption.data('province');
        $("#station_province span").html(province);
        var address = selectedOption.data('address');
        $("#station_address span").html(address);
        $("#longlat span").html("<b>" + app.translate('Latitude:') + ": " + "</b>" + lat + " - <b>" + app.translate('Longitude') + ": " + "</b>" + lon);
        if (stationId && (tabId != '9')) {
            // createChartForAQIWQI(stationId);
            createChartForAQIIndicators(stationId, stationType);
            //createChartForeachIndicators(stationId);
            loadDataForAQIDetail(stationId, stationType);
        }
    });

	$('body').on('click', '.mapMarker', function (e, fromLabel) {
        var currentId = $(e.target).data('id');

        // $('.mapMarker[data-id!=' + currentId + ']').closest('.ol-overlay-container').find('.popover').remove();
        // $('.mapMarker[data-id!=' + currentId + ']').removeAttr("aria-describedby");
        if (e.originalEvent != undefined || fromLabel) {
            // getStationInBackground(currentId, function () {
                $('.mapMarker[data-id!=' + currentId + ']').closest('.ol-overlay-container').find('.popover').closest('.ol-overlay-container').find('.mapMarker').trigger('click');
            // });
        }
        var urlHistorical = "sss";
        urlHistorical += '&' + $.param({station_id: currentId});
        if ($('.mapMarker[data-id=' + currentId + ']').closest('.ol-overlay-container').find('.view-more').length == 0) {
            var buttonHtml = '<a class="view-more"></a>';
            buttonHtml += '<button type="button" class="close closePopover">&times;</button>';
            $('.mapMarker[data-id=' + currentId + ']').closest('.ol-overlay-container').find('.popover').find('.popover-title').append(buttonHtml);

        } else {
        }
        // $(".location-popover").not(this).popover('hide');
        // showHideIndicatorForStation();
    });

	var $map = initMap(json_stations);

    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
    });

    $('body').on('click', '.btnShow', function (e) {
        $('.btnCustomSearch').removeClass('hide');
    });

    $('body').on('click', '.btnChangeOption', function (e) {
        if ($(this).hasClass('active')){
            return false;
        }
        $('.btnChangeOption').removeClass('active');
        $(this).addClass('active');
        var name = $(this).text();
        $('.change-option-title').html(name);
        $('.change-option').find('.row').removeClass('active');
        var opt = $(this).data('option');
        $('.change-option').find('.row[data-option=' + opt + ']').addClass('active');
    });

    $('body').on('click', '.btnChangeType', function (e) {
        if ($(this).hasClass('active')){
            return false;
        }
        $('.btnChangeType').removeClass('active');
        $(this).addClass('active');
        var name = $(this).text();
        $('.change-type-title').html(name);
        var type = $(this).data('type');
        if (!type){
            $('.change-type').find('.ibox').show();
        } else {
            $('.change-type').find('.ibox').hide();
            $('.change-type').find('.ibox[data-type=' + type + ']').show();
        }
    });

    $('body').on('click', '.chkShowHideByStatus input', function (e) {
        var checked = $(this).prop('checked');
        var parent = $(this).closest('.block-status');
        var status = parent.data('status');
        var mapMarker = $('.mapMarker[data-status=' + status + ']');
        var mapLabel = $('.mapLabel[data-status=' + status + ']');
        if (checked){
            mapMarker.show();
        } else {
            mapMarker.hide();
        }
        if ($('.chkShowHideLabel').prop('checked')){
            if (checked){
                // mapLabel.show();
                $('.mapLabel[data-station_type="' + $('#cbbStationType').val() + '"]').show();
            } else {
                mapLabel.hide();
            }
        }
    });

    $('body').on('click', '.collapse-link', function (e) {
        var h = $(this).closest('.ibox').css('height');
        var new_height = 'calc(100% - ' + h + ')!important';
        $('.fh-column.full-height-scroll').css('height', new_height);
    });

    $('body').on('change', '#panelSearchArea', function (e) {
        var url = $(this).data('url');
        var area_id = $(this).val();
        if (area_id){
            showHideMarker($('.mapMarker[data-area_id="' + area_id + '"]'));
        } else {
            showHideMarker($('.mapMarker'));
        }
        var data = {
            station_type: $("#cbbStationType").val(),
            area_id: area_id,
            from_public: 1,
        };
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $('#cbbStations').html(res.html);
                    $('#cbbStations').trigger("chosen:updated");
                    // Set center
                    if (res.latitude_average !== false && res.longitude_average !== false) {
                        map.getView().setCenter(ol.proj.fromLonLat([res.longitude_average, res.latitude_average]));
                        if (area_id) {
                            map.getView().setZoom(6);
                        } else {
                            map.getView().setZoom(6);
                        }
                    }
                }
            }
        });
    });

    $('body').on('change', '#panelSearchProvinces', function (e) {
        var url = $(this).data('url');
        var province_id = $(this).val();
        if (province_id){
            showHideMarker($('.mapMarker[data-province_id="' + province_id + '"][data-station_type="' + $("#cbbStationType").val() + '"]'));
        } else {
            showHideMarker($('.mapMarker[data-station_type="' + $("#cbbStationType").val() + '"]'));
        }
        var data = {
            station_type: $("#cbbStationType").val(),
            province_id: province_id,
            from_public: 1,
            date_time: $("#dt0_from_date").val()
        };
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $('#cbbStations').html(res.html);

                    var firstOption = '';
                    if ($("#cbbStationType").val() == 4) {
                        firstOption = $("#cbbStations option[value='28560877461938780203765592307']").val();
                    } else {
                        firstOption = $("#cbbStations").find("option:first").attr("value");
                    }

                    if (!firstOption) {
                        firstOption = $("#cbbStations").find("option:nth-child(2)").attr("value");
                    }
                    $('#cbbStations').val(firstOption);
                    $('#cbbStations').trigger("change");
                    $('#cbbStations').trigger("chosen:updated");
                    // Set center
                    if (res.latitude_average !== false && res.longitude_average !== false) {
                        map.getView().setCenter(ol.proj.fromLonLat([res.longitude_average, res.latitude_average]));
                        if (province_id) {
                            map.getView().setZoom(6);
                        } else {
                            map.getView().setZoom(6);
                        }
                    }
                }
            }
        });

        loadDataTableListStations();
    });

    $('body').on('click', "ul.station_type li", function () {
        var currentId = $(this).attr('data-id');
        if (currentId == '9') {
            $("#content").hide();
            $("#faq-block").show();
            return;
        }
        else {
            $("#content").show();
            $("#faq-block").hide();

            if (currentId == '4') {
                // // Stack emission or AMBIENT_AIR
                $(".left-block-2").hide();
                $(".left-block-2").css("height", "1px");
                $(".left-block").show();
                $(".tabs-container").show();
                $(".right-block").removeClass("col-md-7");
                $(".right-block").addClass("col-md-8");
                $('.noteForData').html('VN_AQI của thông số trong 7 ngày');
                $('.name_of_table').html('VN_AQI Giờ Trong 7 Ngày');
                $('.name_of_qi').html('VN_AQI giờ');
                $('.name_of_qi_24h').html('VN_AQI ngày');
                $('.type_qi_name').html('VN_AQI');

                // $('#tab-table-data-hour').html('VN_AQI Giờ Trong 24 giờ');
                $('#tab-table-data-hour').show();
                $('#tab-table-data-30day').show();
                $('#tab-table-history').show();
                $("#li-tab-table-data-water_1").hide();
                $("#li-tab-table-data-30day").removeClass("active");
                // $("#li-tab-table-data-hour").addClass("active");

                var hash = '#tab-1';
                $('.nav-tabs a[href="' + hash + '"]').tab('show');

                $('#div_analog_gauge').show();


            } else if ((currentId == '0') || (currentId == '3')) {
                loadDataProvinceHaveStations(currentId);

                $(".left-block").hide();
                $(".left-block-2").show();
                $(".left-block-2").css("height", "auto");
                $(".tabs-container").hide();
                $(".right-block").removeClass("col-md-8");
                $(".right-block").addClass("col-md-7");
                $(".left-block-2").removeClass("hide");

                $("#map>div").empty();
                initMap(json_stations);

                var html = "<div class='panelTieuChuan'>";
                    for (var key in indexItems) {
                        html += "<div  title='" + indexItems[key].text + "' style='background-color: " +
                            indexItems[key].bgColor + "; color: " + indexItems[key].color + ";'><i>";
                        if (indexItems[key]['to']) {
                            html += indexItems[key]['from'] + ' - ' + indexItems[key]['to'];
                        } else {
                            html += 'Trên ' + indexItems[key]['from'];
                        }
                        html += ":</i>&nbsp;<span>" + indexItems[key].text + "</span></div>";
                    }
                    html += "</div>" +
                        "<div class='panelControl'>" +
                        "<label><input class='chkShowHideLabel' type='checkbox'>" + app.translate('Show labels') + "</label>"
                    html += "</div>" +
                        "</div>";
                    $("#map>div").append(html);

                    setInterval(function(){
                        $("#map").css("height", "calc(100% + 400px)");
                        // $("#map div:nth-child(2)").css("height", "calc(100% + 400px)");
                    }, 300);
            } else {
                $(".left-block-2").hide();
                $(".left-block-2").css("height", "1px");
                $(".left-block").show();
                $(".tabs-container").show();
                // // $(".left-block").hide();
                $(".right-block").removeClass("col-md-7");
                $(".right-block").addClass("col-md-8");
                $('.noteForData').html('VN_WQI của thông số trong 7 ngày');
                $('.name_of_table').html('VN_WQI Giờ Trong 7 Ngày');
                $('.name_of_qi').html('VN_WQI giờ');
                $('.name_of_qi_24h').html('VN_AQI ngày');
                $('.type_qi_name').html('VN_WQI');

                // $('#tab-table-data-hour').html('VN_WQI Giờ Trong 24 giờ');
                $('#tab-table-data-hour').hide();
                $('#tab-table-data-30day').hide();
                $('#tab-table-history').hide();
                $("#li-tab-table-data-water_1").show();

                var hash = '#tab-3';
                $('.nav-tabs a[href="' + hash + '"]').tab('show');

            }
        }

        $('#cbbStationType').val(currentId);
        $('#tabId').val(currentId);
        if (currentId === '4') {
            loadDataForAqiColor();
        }

        $("body").find("#panelSearchProvinces").trigger("change");
        $(".mapMarker").hide();
        $(".mapMarker[data-station_type='" + currentId + "']").show();
        $(".mapLabel").hide();
        // $(".mapLabel[data-station_type='" + currentId + "']").show();
        map.getView().setCenter(ol.proj.fromLonLat([106.646397, 17.509177]));
        map.getView().setZoom(6);

        // $(".mapMarker[data-station_type='" + currentId + "']").first().trigger("click");

        // Reload thang mau cho ban do
        json_station_status = $('#json_station_status').html();
        json_station_status = JSON.parse(json_station_status);
        if (currentId == '1') {
            indexItems = $('#json_index_items_wqi').html();
            indexItems = JSON.parse(indexItems);
        } else {
            indexItems = $('#json_index_items').html();
            indexItems = JSON.parse(indexItems);
        }
        json_indicators = $('#json_indicators').html();
        json_indicators = JSON.parse(json_indicators);
        json_stations = $('#json_stations').html();
        json_stations = JSON.parse(json_stations);
        json_area = $('#json_area').html();
        json_area = JSON.parse(json_area);
        json_provinces = $('#json_provinces').html();
        json_provinces = JSON.parse(json_provinces);
        var addCustomFuncitonToMapInterval = setInterval(function () {
            var panelTieuChuan = $("#map>div").find(".panelTieuChuan");
            if (panelTieuChuan.length != 0) {
                panelTieuChuan.remove();
                if ((currentId == '4') || (currentId == '1')) {
                    $("#map").css("height", "calc(100% - 32px)");
                    var html = "<div class='panelTieuChuan'>";
                    for (var key in indexItems) {
                        html += "<div  title='" + indexItems[key].text + "' style='background-color: " +
                            indexItems[key].bgColor + "; color: " + indexItems[key].color + ";'><i>";
                        if (indexItems[key]['to']){
                            html += indexItems[key]['from'] + ' - ' + indexItems[key]['to'];
                        } else {
                            html += 'Trên ' + indexItems[key]['from'];
                        }
                        html += ":</i>&nbsp;<span>" + indexItems[key].text + "</span></div>";
                    }
                    html += "</div>" +
                    "<div class='panelControl'>" +
                     "<label><input class='chkShowHideLabel' type='checkbox'>" + app.translate('Show labels') + "</label>"
                    html += "</div>" +
                    "</div>";
                    $("#map>div").append(html);
                    }
                showHideIndicatorsBar();
                clearInterval(addCustomFuncitonToMapInterval);

            } else {
                if ((currentId == '4') || (currentId == '1')) {
                    $("#map").css("height", "calc(100% - 32px)");
                    var html = "<div class='panelTieuChuan'>";
                    for (var key in indexItems) {
                        html += "<div  title='" + indexItems[key].text + "' style='background-color: " +
                            indexItems[key].bgColor + "; color: " + indexItems[key].color + ";'><i>";
                        if (indexItems[key]['to']) {
                            html += indexItems[key]['from'] + ' - ' + indexItems[key]['to'];
                        } else {
                            html += 'Trên ' + indexItems[key]['from'];
                        }
                        html += ":</i>&nbsp;<span>" + indexItems[key].text + "</span></div>";
                    }
                    html += "</div>" +
                        "<div class='panelControl'>" +
                        "<label><input class='chkShowHideLabel' type='checkbox'>" + app.translate('Show labels') + "</label>"
                    html += "</div>" +
                        "</div>";
                    $("#map>div").append(html);
                }
                showHideIndicatorsBar();
            }
        }, 300);
    });

    $('body').on('click', '#cbbTime', function (e) {
            var url = $(this).data('url');
            var time = $('#dt0_from_date').val()
            var json_stations = '';
            showHideMarker($('.mapMarker'));
            var data = {
                time : time
            };
            app.postAjax({
                url: url,
                data: data,
                callback: function (res) {
                    if (res.success) {
                        json_stations = res.json_stations;
                        json_stations = JSON.parse(json_stations);
                        $('.btnDownload').removeClass('hide');
                        console.log('res',res.json_stations)
                        $("#map>div").empty();
                        initMap(json_stations);
                        console.log('map info', json_stations);
                        // set zoom for map
                        map.getView().setZoom(6);
                    }
                }
            });

            // Show/hide indicators on panel
            $('.toolParameters .items .item').prop('checked', false);
            $('.toolParameters .items .item').hide();
            $('.toolParameters .items .item[data-type="' + station_type + '"]').show();
        });

    // Show chart on left bar
    var stationId  = $('#cbbStations').val();
    var tabId  = $('#tabId').val();

    if (stationId && (tabId != '9')) {
        //createChartForAQIWQI(stationId);
        //createChartForeachIndicators(stationId);
        createChartForAQIIndicators(stationId, stationType);
        loadDataForAQIDetail(stationId, stationType);
    }
    //loadDataForAqiColor();
    initAnalogGauge();
    // Show station by type
    $("ul.station_type li.active").trigger("click");
    loadDataTableForPage();
    loadDataTableForPage_24h();
    loadDataTableForPageWater_1();
    loadDataTableListStations();

    //
    // Analog gauge
    // loadDataForAqiColor();
    // initAnalogGauge();
});

function showHideMarker(markers) {
    var total = markers.length;
    $('.mapMarker').hide();
    $('.mapLabel').hide();
    for (var i=0; i<total; i++){
        var stationId = $(markers[i]).data('id');
        $(markers[i]).show();
        $('.mapLabel[data-id="' + stationId + '"]').show();
    }
}

function getColorForTextIndex($idx) {
    var color = '#000';
    for (var key in indexItems) {
        if(indexItems[key].from <= $idx){
            if (indexItems[key].to != undefined){
                if (indexItems[key].to >= $idx){
                    color = indexItems[key].bgColor;
                    break;
                }
            } else {
                color = indexItems[key].bgColor;
                break;
            }
        }
    }
    return color;
}

function getStatusForTextIndex($idx) {
    var text = '';
    for (var key in indexItems) {
        if(indexItems[key].from <= $idx){
            if (indexItems[key].to != undefined){
                if (indexItems[key].to >= $idx){
                    text = "(" + indexItems[key].text + ")";
                    break;
                }
            } else {
                text = "(" + indexItems[key].text + ")";
                break;
            }
        }
    }
    return text;
}

function getColorForIndex($idx) {
    var color = '#000';
    for (var key in indexItems) {
        if(indexItems[key].from <= $idx){
            if (indexItems[key].to != undefined){
                if (indexItems[key].to >= $idx){
                    color = indexItems[key].color;
                    break;
                }
            } else {
                color = indexItems[key].color;
                break;
            }
        }
    }
    return color;
}

function getBgForIndex($idx) {
    var bg = '#fff';
    for (var key in indexItems) {
        if(indexItems[key].from <= $idx){
            if (indexItems[key].to != undefined){
                if (indexItems[key].to >= $idx){
                    bg = indexItems[key].bg;
                    break;
                }
            } else {
                bg = indexItems[key].bg;
                break;
            }
        }
    }
    return bg;
}

function initMap(markers_json) {
    map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Group({
                'title': 'Base maps',
                layers: [
                   new ol.layer.Tile({
                        title: 'VietBanDo',
                        visible: true,
                        type: 'base',
                        source: new ol.source.XYZ({
//                              crossOrigin: 'anonymous',
                              crossOrigin: null,
                              attributions: 'Copyright:© 2013 ESRI, i-cubed, GeoEye',
                              url:'https://map.hap-technology.com/ImageLoader/GetImage.ashx?Ver=2016&LayerIds=VBD&Level={z}&X={x}&Y={y}'
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Map',
                        visible: false,
                        type: 'base',
                        source: new ol.source.BingMaps({
                            key: 'As1HiMj1PvLPlqc_gtM7AqZfBL8ZL3VrjaS3zIb22Uvb9WKhuJObROC-qUpa81U5',
                            imagerySet: 'Road'
                        })
                    }),
                    new ol.layer.Tile({
                        title: 'Bản đồ nền',
                        visible: false,
                        source: new ol.source.TileArcGISRest({
                            projection: 'EPSG:4326',
                            url: 'http://bando.cem.gov.vn/ArcGIS/rest/services/DauMang_Phase2/dauMang_ToanQuoc/MapServer'
                        })
                    }),
                ]
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([106.646397, 17.509177]),
            zoom: 9
        })
    });

    // An lop bien trung quoc
    var jsonData = [{
        lat: 8.485053,
        lng: 107.829848
        },
        {
            lat: 8.398115,
            lng: 102.732192
        },
        {
            lat: 6.131456,
            lng: 102.776137
        },
        {
            lat: 5.34441,
            lng: 106.072035
        },
        {
            lat: 4.862929,
            lng: 108.18141
        },
        {
            lat: 5.388162,
            lng: 111.301528
        },
        {
            lat: 6.917342,
            lng: 109.719496
        }
    ]
    // A ring must be closed, that is its last coordinate
    // should be the same as its first coordinate.
    var ring = [];
    for (var i = 0; i < jsonData.length; i++) {
        ring.push([jsonData[i].lng, jsonData[i].lat]);
    }
    // A polygon is an array of rings, the first ring is
    // the exterior ring, the others are the interior rings.
    // In your case there is one ring only.
    var polygon = new ol.geom.Polygon([ring]);
    polygon.transform('EPSG:4326', 'EPSG:3857');

    // Create feature with polygon.
    var feature = new ol.Feature(polygon);
    feature.set('name', 'polygon');

    // Create vector source and the feature to it.
    var vectorSource = new ol.source.Vector();
    vectorSource.addFeature(feature);

    var style = [
        /* We are using two different styles for the polygons:
         *  - The first style is for the polygons themselves.
         *  - The second style is to draw the vertices of the polygons.
         *    In a custom `geometry` function the vertices of a polygon are
         *    returned as `MultiPoint` geometry, which will be used to render
         *    the style.
         */
        new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: '#AAC5F0',
                width: 3
            }),
            fill: new ol.style.Fill({
                color: '#AAC5F0'
            })
        }),
        new ol.style.Style({
            image: new ol.style.Circle({
                radius: 2,
                fill: new ol.style.Fill({
                    color: '#AAC5F0'
                })
            }),
            geometry: function (feature) {
                // return the coordinates of the first ring of the polygon
                var coordinates = feature.getGeometry().getCoordinates()[0];
                return new ol.geom.MultiPoint(coordinates);
            }
        })
    ];

    // Create vector layer attached to the vector source.
    var vectorLayer = new ol.layer.Vector({
        source: vectorSource,
        style: style
    });

    // Add the vector layer to the map.
    // map.addLayer(vectorLayer);

    var tooltip = document.getElementById('tooltip');
    var overlay = new ol.Overlay({
        element: tooltip,
        offset: [10, 0],
        positioning: 'bottom-left'
    });
    map.addOverlay(overlay);

    // Hoang Sa
    var pos = ol.proj.fromLonLat([112.488568, 14.808077]);

    // Hoang sa marker
    var marker = new ol.Overlay({
        position: pos,
        positioning: 'center-center',
        element: document.getElementById('marker'),
        stopEvent: false
    });
    map.addOverlay(marker);

    var hoangsa = new ol.Overlay({
        position: pos,
        element: document.getElementById('hoangsa')
    });
    map.addOverlay(hoangsa);

    //Full Screen
    var myFullScreenControl = new ol.control.FullScreen();
    map.addControl(myFullScreenControl);

    var layerSwitcher = new ol.control.LayerSwitcher({
        tipLabel: app.translate('Layer Switcher')
    });
    map.addControl(layerSwitcher);

    for (var key in markers_json) {
        if (markers_json.hasOwnProperty(key)) {
            var point = markers_json[key];
            if (point.station_type == 4 || point.station_type == 1) {
                var html =
                    "<div class=\"modal-dialog modal-md\">" +
                    "<div class=\"modal-content\">" +
                    "<div class=\"modal-header\">" +
                    "<button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button>" +
                    "<h4 class=\"modal-title\">Sumary info</h4>" +
                    "</div>" +
                    "<div class=\"modal-body\">" +
                    "<div class=\"row\"><div class=\"col-sm-4 custom-index\" style=\"background-color: " +
                    point.bgColor + "; color: " + point.Color + "\">" + point.index +
                    "</div><div class=\"col-sm-8\"><span class=\"custom-name\" style=\"color: " + point.bgColor + "\">" + point.station_name +
                    "</span><div>updated an hour ago<br><i>(2018-10-05 10:10:10)</i></div></div></div>" +
                    "<div class=\"row custom-image text-center\"><img src=\"../static/views/qi/air_" + (Math.floor(Math.random() * 5) + 1) + ".png\"></div>" +
                    "</div>" +
                    "</div>";
                var totalParams = point.parameters.length;
                for (var j = 0; j < totalParams; j++) {
                    var parameter = point.parameters[j];
                    // html += "<tr><td>" + (j + 1).toString() + "</td><td>" + parameter.key + "</td><td>" + parameter.value + "</td><td>" + parameter.unit + "</td></tr>";
                }
                var pos = ol.proj.fromLonLat(point.lonlat);
                var contentPopover = app.translate('Index') + ": <span class=\"custom-index-popover\" style=\"background-color: " + point.bgColor +
                    "; color: " + point.color + "\">" + point.index + "<i> " + point.status_text + " </i>" + "</span><br />";

                if (point.index == null || point.index == "-") {
                    contentPopover += "<div class=\"text-center\">" + app.translate('No data') + "</div>";
                } else {
                    contentPopover += "<div class=\"text-center\"></div>";
                }

                if (point.qi_time) {
                    contentPopover += "<div class=\"text-center\">" + point.qi_time + "</div>";
                }
                contentPopover += "<hr style=\"margin: 10px 0px 0px\"><div class=\"text-center\"><i>" + app.translate('click for more information') + "</i></div>";
                var selector = "<div class='mapMarker' data-status='" + point.status + "' data-id='" + point.station_id + "' title='" + point.station_name + "'" +
                    " style='background-color: " + point.bgColor + "; color: " + point.color + "'" +
                    ' data-station_type="' + point.station_type + '" data-province_id="' + point.province_id + '"' +
                    ' data-area_id="' + point.area_id + '" ' +
                    " data-content='" + html + "'>" + point.index + "</div>";
                // point
                var marker = new ol.Overlay({
                    position: pos,
                    positioning: 'center-center',
                    // element: document.getElementById('marker'),
                    element: $(selector).on('click', function (e, fromLabel) {
                        var content = $(this).data('content');
                        // $('#myModal').html(content).modal(); // Todo: Uncomment for show popup

                        // // Show chart on left bar
                        // var station_id = $(this).data('id');
                        // $('#cbbStations').val(station_id);
                        // $('#cbbStations').trigger("chosen:updated");
                        // createChartForAQIIndicators(station_id);
                        // createChartForeachIndicators(station_id);
                    })[0],
                    stopEvent: false
                });
                map.addOverlay(marker);

                // label
                html = "<h4 class='custom-popover' title='" + point.station_name + "' data-content='" + contentPopover + "'>" + point.station_name + "</h4>";
                for (var j = 0; j < totalParams; j++) {
                    var parameter = point.parameters[j];
                    html += "<p class='param' data-id='" + parameter['id'] + "' style='display: none'>" + parameter['key'] + ": " + parameter['value'] + " " + parameter['unit'] + "</p>";
                }
                var label = new ol.Overlay({
                    position: pos,
                    element: $("<div id='mapLabel' data-station_type='" + point.station_type + "' data-status='" + point.status + "' data-id='" + point.station_id + "' class='mapLabel'>").html(html)[0],
                    stopEvent: false,
                });
                map.addOverlay(label);
            } else {
                var html =
                    "<div class=\"modal-dialog modal-md\">" +
                    "<div class=\"modal-content\">" +
                    "<div class=\"modal-header\">" +
                    "<button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button>" +
                    "<h4 class=\"modal-title\">Sumary info</h4>" +
                    "</div>" +
                    "<div class=\"modal-body\">" +
                    "<div class=\"row\"><div class=\"col-sm-4 custom-index\" style=\"background-color: " +
                    point.bgColor + "; color: " + point.Color + "\">" + point.index +
                    "</div><div class=\"col-sm-8\"><span class=\"custom-name\" style=\"color: " + point.bgColor + "\">" + point.station_name +
                    "</span><div>updated an hour ago<br><i>(2018-10-05 10:10:10)</i></div></div></div>" +
                    "<div class=\"row custom-image text-center\"><img src=\"../static/views/qi/air_" + (Math.floor(Math.random() * 5) + 1) + ".png\"></div>" +
                    "</div>" +
                    "</div>";
                var totalParams = point.parameters.length;
                for (var j = 0; j < totalParams; j++) {
                    var parameter = point.parameters[j];
                    html += "<tr><td>" + (j + 1).toString() + "</td><td>" + parameter.key + "</td><td>" + parameter.value + "</td><td>" + parameter.unit + "</td></tr>";
                }
                var pos = ol.proj.fromLonLat(point.lonlat);
                var contentPopover = app.translate('Index') + ": <span class=\"custom-index-popover\" style=\"background-color: " + point.bgColor +
                    "; color: " + point.color + "\">" + point.index + "<i> " + point.status_text + " </i>" + "</span><br />";

                if (point.index == null || point.index == "-") {
                    contentPopover += "<div class=\"text-center\">" + app.translate('No data') + "</div>";
                } else {
                    contentPopover += "<div class=\"text-center\"></div>";
                }

                if (point.qi_time) {
                    contentPopover += "<div class=\"text-center\">" + point.qi_time + "</div>";
                }
                contentPopover += "<hr style=\"margin: 10px 0px 0px\"><div class=\"text-center\"><i>" + app.translate('click for more information') + "</i></div>";

                var htmlContentPopover =
                                "<div><b>" + app.translate('Station Code:') + " </b> " + point.station_code + "</div>" +
                                "<div><b>" + app.translate('Province:') + " </b> " + point.province_name + "</div>" +
                                "<div><b>" + app.translate('Address:') + " </b> " + point.address + "</div>" +
                                "<div><b>" + app.translate('Latitude:') + " </b> " + point.lonlat[1] + " - <b>" + app.translate('Longitude') + "</b> " + point.lonlat[0] + "</div>" +
                                "<div><b>" + app.translate('Status:') + ":</b> <b style=\"display: font-size: 1.2em; color:" + json_station_status[point.status]['color'] + "\">" + app.translate(point.status_disp) + "</b></div>";
                var htmlIndicator = '';
                var totalParams = point.indicator_list.length;
                    for (var j = 0; j < totalParams; j++) {
                        var parameter = point.indicator_list[j];
                        if (parameter != null) {
                             if (parameter.value != '') {
                                htmlIndicator += "<span style='color: " + parameter.color + "'>" + parameter.value + "</span>";
                                if (j < (point.indicator_list.length - 1)) {
                                    htmlIndicator += ", ";
                                }
                            }
                        }
                    }
                htmlContentPopover += "</br><div><b>Thông số:</b> <b >" + htmlIndicator + "</b></div>";

                var selector = '<div id="' + point.station_id + '" class="mapMarker" data-status="' + point.status + '" data-id="' + point.station_id + '" title="' + point.station_name + '"'+
                                ' style="background-color: ' + json_station_status[point.status]['color'] + '"'+
                                ' data-station_type="' + point.station_type + '" data-province_id="' + point.province_id + '"'+
                                ' data-area_id="' + point.area_id + '">';
                // point
                var marker = new ol.Overlay({
                    position: pos,
                    positioning: 'center-center',
                    // element: document.getElementById('marker'),
                    element: $(selector).on('click', function (e, fromLabel) {
                        var content = $(this).data('content');
                        // $('#myModal').html(content).modal(); // Todo: Uncomment for show popup

                        // // Show chart on left bar
                        // var station_id = $(this).data('id');
                        // $('#cbbStations').val(station_id);
                        // $('#cbbStations').trigger("chosen:updated");
                        // createChartForAQIIndicators(station_id);
                        // createChartForeachIndicators(station_id);
                    })[0],
                    stopEvent: false
                });

                // point
                var marker = new ol.Overlay({
                    position: pos,
                    positioning: 'center-center',
                    element: $(selector).popover({
                        'placement': 'left',
                        'html': true,
                        'content': htmlContentPopover,
                    })[0],
                    stopEvent: false
                });
                map.addOverlay(marker);

                // label
                html = "<h4 class='custom-popover' title='" + point.station_name + "' data-content=''>" + point.station_name + "</h4>";
                for (var j = 0; j < totalParams; j++) {
                    var parameter = point.parameters[j];
                    // html += "<p class='param' data-id='" + parameter['id'] + "' >" + parameter['key'] + ": " + parameter['value'] + " " + parameter['unit'] + "</p>";
                }
                var label = new ol.Overlay({
                    position: pos,
                    element: $("<div id='mapLabel' data-station_type='" + point.station_type + "' data-status='" + point.status + "' data-id='" + point.station_id + "' class='mapLabel'>").html(html)[0],
                    stopEvent: false,
                });
                map.addOverlay(label);
            }
        }
    }

    var template = '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-title"></div>' +
        '<div class="popover-content" style="min-width: 50px;"></div></div>';
    $(".custom-popover").popover({
        animation : true,
        placement: 'auto top',
        html: true,
        container: 'body',
        template: template,
        trigger: 'hover'
    });

    if (false) {
        // Popup showing the position the user clicked
        var popup = new ol.Overlay({
            element: document.getElementById('popup')
        });
        map.addOverlay(popup);

        map.on('click', function (evt) {
            console.log(evt.pixel);
            var element = popup.getElement();
            var coordinate = evt.coordinate;
            var hdms = ol.coordinate.toStringHDMS(ol.proj.toLonLat(coordinate));

            $(element).popover('destroy');
            popup.setPosition(coordinate);
            $(element).popover({
                placement: 'top',
                animation: false,
                html: true,
                content: '<p>The location you clicked was:</p><code>' + hdms + '</code>'
            });
            $(element).popover('show');
        });
    }
    return map
}

function showHideIndicatorsBar(){
    var stationType = $('#cbbStationType').val();
    $('.toolParameters').find('.item').hide();
    $('.toolParameters').find('.item[data-type="' + stationType + '"]').show();
}

function createChartForAQIWQI(station_id) {
    // Call action to redraw right panel
    var url = $('#aqi_detail').attr("data-url");

    url += "?" + $.param({station_id: station_id});
    $("#aqi_detail").load(url);
}

function createChartForeachIndicators(station_id) {
    var url = $('#hfUrlGetChartForStation').val();
    app.postAjax({
        showProgress: false,
        url: url,
        data: {station_id: station_id, from_public: 1},
        callback: function (res) {
            var charts = res.charts;
            $('.station_name_detail').html(res.station_name);
            $('.last_check_detail').html(res.last_check);
            $('.all-charts').html('');

            for (var k in charts) {
                var html = '<div class="flot-chart-content" id="flot-bar-chart-' + k + '"></div><div class="clearfix"></div> ';
                $('.all-charts').append(html);
                // Create the COLUMNE chart
                var series_data = charts[k];
                var subtitle = '';
                Highcharts.chart('flot-bar-chart-' + k, {
                    chart: {
                        type: 'column',
                        backgroundColor: '#FFFFFF'
                    },
                    credits: {
                        enabled: false
                    },
                    title: {
                        text: '<b>' + k + '</b>'
                    },
                    subtitle: {
                        text: subtitle
                    },
                    xAxis: {
                        // type: 'datetime',
                        // dateTimeLabelFormats: {day: '%e. %b'}
                        visible: false,
                        title: {
                            enabled: null,
                            text: null
                        }
                    },
                    yAxis: {
                        enabled: false,
                        title: {
                            enabled: null,
                            text: null
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        series: {
                            borderWidth: 0,
                            dataLabels: {
                                enabled: true,
                                format: '{point.y}'
                            }
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
                        pointFormat: '<b>{point.y}</b><br/>'
                    },
                    series: [
                        {
                            "name": app.translate("AQI in 7 days"),
                            "colorByPoint": true,
                            data: series_data,
                        }
                    ]
                });
            }
        }
    });
}

function createChartForAQIIndicators(stationId, stationType) {
    if ($('#tabId').val() == '9') {
        return;
    }
    if (stationType == 4 || stationType == 1) {
        var url = $('#detailChartWidgetAqi').data('url');
        app.postAjax({
            showProgress: false,
            url: url,
            data: {station_id: stationId, from_public: 1, station_type: stationType},
            callback: function (res) {
                var bgColor = 'green';
                if (res.aqi_detail_info && res.aqi_detail_info.bgColor) {
                    bgColor = res.aqi_detail_info.bgColor;
                }
                var color = 'white';
                if (res.aqi_detail_info && res.aqi_detail_info.color) {
                    color = res.aqi_detail_info.color;
                }
                $('.indicator-value-wrap').css({'background': bgColor});
                $('.indicator-value-wrap .indicator-value').css({'color': color});
                $('#div_analog_gauge').show();
                if (res.aqi == '-'){
                    // $('#div_analog_gauge').hide();
                    // $('#div_analog_gauge_24h').hide();
                } else if (res.aqi == 'wqi') {
                    // $('#div_analog_gauge_24h').show();
                    $('#div_analog_gauge').hide();
                    // $('#div_analog_gauge_24h .number-chart').css({'visibility': 'hidden'});
                    // $('#div_analog_gauge .number-chart').addClass("hidden-class");
                    // $('#div_analog_gauge').addClass("hidden-class");
                } else {
                    $('#div_analog_gauge').show();
                    // $('#div_analog_gauge_24h').show();
                    // $('#div_analog_gauge_24h .number-chart').removeClass("hidden-class")
                    // $('#div_analog_gauge .number-chart').removeClass("hidden-class")
                    // $('#div_analog_gauge').show();
                    // $('#div_analog_gauge_24h .number-chart').show();
                    // $('#div_analog_gauge_24h .number-chart').css({'visibility': 'unset'});
                }
                $('.widget_aqi_info .indicator-value').html(res.aqi);
                $('.widget_aqi_info .at-time').html(res.at_time);
                $('.widget_aqi_info .at-date').html(res.at_date);
                var chart = res.chart;
                var chart_data = [];
                if (chart.series && chart.series[0]){
                    chart_data = chart.series[0].data;
                }
                Highcharts.chart('detailChartWidgetAqi', {
                    chart: {
                        type: 'bar',
                    },
                    title: chart.title,
                    subtitle: chart.subtitle,
                    xAxis: {
                        categories: chart.categories
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: ''
                        }
                    },
                    credits: {
                        enabled: false
                    },
                    legend: {
                        enabled: false,
                        reversed: true
                    },
                    plotOptions: {
                        series: {
                            stacking: 'normal'
                        }
                    },
                    series: [{
                        name: app.translate('AQI Indicators'),
                        data: chart_data
                    }]
                });
                if (res.lat && res.lon){
                    if (stationType == '4' || stationType == '1') {
                        var url_res = 'http://api.openweathermap.org/data/2.5/weather?lat=' + res.lat + '&lon=' + res.lon + '&appid=b3c6503ac31cb5e72765e98cd0d7795e&units=metric&lang=vi&cnt=64';
                        app.postAjax({
                            url: url_res,
                            callback: function (res2) {
                                $('.weather .temp label span').html(res2.main.temp);
                                $('.weather .humidity label span').html(res2.main.humidity);
                                $('.weather .wind label span').html(res2.wind.speed);
                                $('.weather .pressure label span').html(res2.main.pressure);
                            }
                        });
                    }
                }
            }
        });

        // Load added columns - For 30 days, For Hour
        var url = $("#hfURLLoadIndicator").val();
        app.postAjax({
            url: url,
            data: {station_id : stationId, from_public: 1, station_type: stationType},
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedColumns').html(res.html);
                    $('#cbbAddedColumns').trigger("change");
                    $('#cbbAddedColumns').trigger("chosen:updated");
                    // oTable[0].fnFilter('');
                    loadDataTableForPage();

                    $('#cbbAddedColumns_1').html(res.html);
                    $('#cbbAddedColumns_1').trigger("change");
                    $('#cbbAddedColumns_1').trigger("chosen:updated");
                    loadDataTableForPage_24h();

                    $('#cbbAddedColumns_2').html(res.html);
                    $('#cbbAddedColumns_2').trigger("change");
                    $('#cbbAddedColumns_2').trigger("chosen:updated");
                    loadDataTableForPageWater_1();

                } else {
                    app.showError(res.message);
                }
            }
        });

        // for hour
        // app.postAjax({
        //     url: url,
        //     data: {station_id : stationId, from_public: 1, station_type: stationType},
        //     callback: function (res) {
        //         if (res.success) {
        //             $('#cbbAddedColumns_1').html(res.html);
        //             $('#cbbAddedColumns_1').trigger("change");
        //             $('#cbbAddedColumns_1').trigger("chosen:updated");
        //
        //             // oTable[1].fnFilter('');
        //             // oTable[1].fnFilter('');
        //             loadDataTableForPage_24h();
        //         } else {
        //             app.showError(res.message);
        //         }
        //     }
        // });
    }
}

var hand = null;
var hand24h = null;
var chart = null;
var chart24h = null;
var labelAMChart = null;
var labelAMChart24h = null;
var labelAMChartTime = null;
var labelAMChartTime24h = null;
var ranges = [];
function initAnalogGauge(qi_colors, max_value) {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end

    // create chart
    chart = am4core.create("analog_gauge", am4charts.GaugeChart);
    chart.hiddenState.properties.opacity = 0; // this makes initial fade in effect

    chart.innerRadius = -50;

    var axis = chart.xAxes.push(new am4charts.ValueAxis());
    axis.min = 0;
    axis.max = max_value;
    axis.renderer.inside = true;
    axis.strictMinMax = true;
    axis.valueInterval = 100;
    axis.renderer.grid.template.stroke = new am4core.InterfaceColorSet().getFor("background");
    axis.renderer.grid.template.strokeOpacity = 0.3;
    axis.renderer.labels.template.radius = -5;
    axis.renderer.grid.template.disabled = true;
    axis.renderer.labels.template.adapter.add("text", function(text) {
        return text;
    });

    /**
     * Label
     */

    labelAMChart = chart.radarContainer.createChild(am4core.Label);
    labelAMChart.isMeasured = false;
    labelAMChart.fontSize = 50;
    labelAMChart.color = 'red';
    labelAMChart.fontWeight = 'bolder';
    labelAMChart.x = am4core.percent(10);
    labelAMChart.y = am4core.percent(50);
    labelAMChart.horizontalCenter = "middle";
    labelAMChart.verticalCenter = "bottom";
    labelAMChart.text = "";

    for(var k in qi_colors) {
        var range0 = axis.axisRanges.create();
        range0.value = qi_colors[k]['from'];
        range0.endValue = qi_colors[k]['to'];
        range0.axisFill.fillOpacity = 1;
        range0.axisFill.fill = qi_colors[k]['color'];
        range0.axisFill.zIndex = -1;
        ranges.push(range0);
    }

    labelAMChartTime = chart.radarContainer.createChild(am4core.Label);
    labelAMChartTime.isMeasured = false;
    // labelAMChartTime.fontSize = 30;
    // labelAMChartTime.color = '';
    // labelAMChartTime.fontWeight = 'bold';
    labelAMChartTime.x = am4core.percent(10);
    labelAMChartTime.y = 10;
    labelAMChartTime.horizontalCenter = "middle";
    labelAMChartTime.verticalCenter = "top";
    labelAMChartTime.marginTop = 20;
    labelAMChartTime.text = "-";

    var axis2 = chart.xAxes.push(new am4charts.ValueAxis());
    axis2.min = 0;
    axis2.max = max_value;
    axis2.renderer.innerRadius = 10;
    axis2.strictMinMax = true;
    axis2.renderer.labels.template.disabled = true;
    axis2.renderer.ticks.template.disabled = true;
    axis2.renderer.grid.template.disabled = true;

    hand = chart.hands.push(new am4charts.ClockHand());
    hand.axis = axis2;
    hand.innerRadius = am4core.percent(30);
    hand.startWidth = 10;
    hand.pin.disabled = true;
    hand.value = 50;
    // chart.handleResize();

    // For 24h
    chart24h = am4core.create("analog_gauge_24h", am4charts.GaugeChart);
    chart24h.hiddenState.properties.opacity = 0; // this makes initial fade in effect

    chart24h.innerRadius = -50;

    var axis24h = chart24h.xAxes.push(new am4charts.ValueAxis());
    axis24h.min = 0;
    axis24h.max = max_value;
    axis24h.renderer.inside = true;
    axis24h.strictMinMax = true;
    axis24h.valueInterval = 100;
    axis24h.renderer.grid.template.stroke = new am4core.InterfaceColorSet().getFor("background");
    axis24h.renderer.grid.template.strokeOpacity = 0.3;
    axis24h.renderer.labels.template.radius = -5;
    axis24h.renderer.grid.template.disabled = true;
    axis24h.renderer.labels.template.adapter.add("text", function(text) {
        return text;
    });

    /**
     * Label
     */

    labelAMChart24h = chart24h.radarContainer.createChild(am4core.Label);
    labelAMChart24h.isMeasured = false;
    labelAMChart24h.fontSize = 50;
    labelAMChart24h.color = 'red';
    labelAMChart24h.fontWeight = 'bolder';
    labelAMChart24h.x = am4core.percent(10);
    labelAMChart24h.y = am4core.percent(50);
    labelAMChart24h.horizontalCenter = "middle";
    labelAMChart24h.verticalCenter = "bottom";
    labelAMChart24h.text = "";

    for(var k in qi_colors) {
        var range0 = axis24h.axisRanges.create();
        range0.value = qi_colors[k]['from'];
        range0.endValue = qi_colors[k]['to'];
        range0.axisFill.fillOpacity = 1;
        range0.axisFill.fill = qi_colors[k]['color'];
        range0.axisFill.zIndex = -1;
        ranges.push(range0);
    }

    labelAMChartTime24h = chart24h.radarContainer.createChild(am4core.Label);
    labelAMChartTime24h.isMeasured = false;
    labelAMChartTime24h.x = am4core.percent(10);
    labelAMChartTime24h.y = 10;
    labelAMChartTime24h.horizontalCenter = "middle";
    labelAMChartTime24h.verticalCenter = "top";
    labelAMChartTime24h.text = "-";

    var axisTime24h = chart24h.xAxes.push(new am4charts.ValueAxis());
    axisTime24h.min = 0;
    axisTime24h.max = max_value;
    axisTime24h.renderer.innerRadius = 10;
    axisTime24h.strictMinMax = true;
    axisTime24h.renderer.labels.template.disabled = true;
    axisTime24h.renderer.ticks.template.disabled = true;
    axisTime24h.renderer.grid.template.disabled = true;

    hand24h = chart24h.hands.push(new am4charts.ClockHand());
    hand24h.axis = axisTime24h;
    hand24h.innerRadius = am4core.percent(30);
    hand24h.startWidth = 10;
    hand24h.pin.disabled = true;
    hand24h.value = 50;
}

function loadDataForAqiColor() {
    $('.list-info-chart').html('');
    var url = siteUrl + '/services/call/json/get_common_settings';
    var payload  = {
    };
    var stationType  = $('#cbbStationType').val();
    // Load data for block 1
    $.ajax({
        type: "POST",
        dataType: 'json',
        url: url,
        data: payload,
        async: true,
        processData: true,
        contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
        enctype: 'multipart/form-data',
        success: function(data){
            if (data.success){
                if (stationType == 1) {
                    $('.list-info-chart').html('');
                    for (var k in data.wqi_colors){
                        var li = '<li><span class="box-square" style="background: ' + data.wqi_colors[k]['color'] + '"></span>' + data.wqi_colors[k]['name'] + '</li>';
                        $('.list-info-chart').append(li);
				    }
				    initAnalogGauge(data.wqi_colors, 100);

                } else {
                    $('.list-info-chart').html('');
                    for (var k in data.qi_colors){
                        var li = '<li><span class="box-square" style="background: ' + data.qi_colors[k]['color'] + '"></span>' + data.qi_colors[k]['name'] + '</li>';
                        $('.list-info-chart').append(li);
                    }
				    initAnalogGauge(data.qi_colors, 500);
                }
            }
        },
    });
}

function loadDataForAQIDetail(station_id, station_type) {
    var sparkBarWidthValue = 8;
    if ($(window).width() < 991 && $(window).width() > 590) {
        sparkBarWidthValue = 8;
    } else if ($(window).width() < 460 && $(window).width() >= 360) {
        sparkBarWidthValue = 7;
    } else if ($(window).width() < 360) {
        sparkBarWidthValue = 6;
    } else {
        sparkBarWidthValue = 8;
    }

    $('#box-2 .table-chart tbody').html('');
    $('#box-3 .table-chart tbody').html('');
    if (station_type == 4 || station_type == 1) {
        // $('#block_stations_indicator').html('');
        var url = siteUrl + '/services/call/json/qi_detail_for_eip';
        var payload  = {
            station_id: station_id,
            station_type: station_type,
        };
        // Load data for block 1
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: url,
            data: payload,
            async: true,
            processData: true,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            enctype: 'multipart/form-data',
            success: function(data){
                if (data.success){
                    var row = '';
                    var myObj = data.res,
                        keys = Object.keys(myObj),
                        i, len = keys.length;
                    keys.sort();
                    var lengthData = 0;
                    var qi_time_2 = data['qi_time_2'];

                    if (station_type == 1) {
                        title_qi = "VN WQI: ";
                    } else {
                        title_qi = "VN AQI: ";
                    }
                    for (i = 0; i < len; i++) {
                        k = keys[i];
                        var sparklinesClass = 'sparklines sparklines-' + k;
                        var box2Sparklines = '#box-2 .sparklines-' + k;
                        if (lengthData == 0) {
                            lengthData = myObj[k]['values'].length;
                        }
                        var dataConvert = createTimeLookupsAQIChart(myObj[k]['values']);

                        if (["PM-10", "PM-2-5"].includes(k)) {
                            kText = k;
                            if (k == "PM-2-5") {
                                kText = "PM-2.5";
                            }
                            if (true) {
                                var tr = '<tr>';
                                tr += '<td>' + kText + '</td>';
                                tr += '<td>' + Math.round(myObj[k]['current']) + '</td>';
                                tr += '<td><span class="' + sparklinesClass + '" ' + 'sparkHeight="24px" sparkBarWidth="' + sparkBarWidthValue + '" sparkChartRangeMin="0" sparkType="bar" >' + dataConvert['dataValues'].join(',') + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['min']) + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['max']) + '</span></td>';
                                tr += '</tr>';
                                $('#box-2 .table-chart tbody').append(tr);
                            }

                            $(box2Sparklines).sparkline('html', {
                                enableTagOptions: true,
                                colorMap: data.color_map,
                                tooltipFormat: title_qi + "{{value:val}} ,  {{offset:timeLookup}}",
                                tooltipValueLookups: {
                                    "val": {"-1": "N/A"},
                                    "timeLookup": dataConvert['dataTimes'],
                                }
                            });
                        }
                    }
                    for (i = 0; i < len; i++) {
                        k = keys[i];
                        var sparklinesClass = 'sparklines sparklines-' + k;
                        var box2Sparklines = '#box-2 .sparklines-' + k;
                        var dataConvert = createTimeLookupsAQIChart(myObj[k]['values']);
                        if (!["PM-10", "PM-2-5"].includes(k)) {
                            if (true && Math.round(myObj[k]['max'] > 0)) {
                                var tr = '<tr>';
                                tr += '<td>' + k + '</td>';
                                tr += '<td>' + Math.round(myObj[k]['current']) + '</td>';
                                tr += '<td><span class="' + sparklinesClass + '" ' + 'sparkHeight="24px" sparkBarWidth="' + sparkBarWidthValue +  '" sparkChartRangeMin="0" sparkType="bar" >' + dataConvert['dataValues'].join(',') + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['min']) + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['max']) + '</span></td>';
                                tr += '</tr>';
                                $('#box-2 .table-chart tbody').append(tr);
                            }

                            $(box2Sparklines).sparkline('html', {
                                enableTagOptions: true,
                                colorMap: data.color_map,
                                tooltipFormat: title_qi + "{{value:val}} ,  {{offset:timeLookup}}",
                                tooltipValueLookups: {
                                    "val": {"-1": "N/A"},
                                    "timeLookup": dataConvert['dataTimes'],
                                }
                            });
                        }
                    }

                    // Display start date - end date chart
                    $('#start_date_aqi').empty();
                    $('#end_date_aqi').empty();
                    $('#mid_date_aqi').empty();
                    $('#start_date_aqi').append(startEndTimeChart(lengthData - 1, qi_time_2, false));
                    $('#end_date_aqi').append(startEndTimeChart(0, qi_time_2, false));
                    $('#mid_date_aqi').append(startEndTimeChart(lengthData / 2, qi_time_2, true));

                    hand.showValue(Number(data.qi_value), am4core.ease.cubicOut);
                    title_station_name = '';
                    title_qi_box2= '';
                    if (station_type == 1) {
                        title_station_name = "VN_WQI Giờ: ";
                        title_qi_box2 = "VN_WQI Giờ theo từng thông số";
                    } else {
                        title_station_name = "VN_AQI Giờ: ";
                        title_qi_box2 = "VN_AQI Giờ theo từng thông số";
                    }

                    $('#name_tram').html(title_station_name + data.station_name);
                    $('#title_qi_box2').html(title_qi_box2);
                    labelAMChart.text = data.qi_value;
                    labelAMChart.fill = am4core.color('#000');
                    labelAMChart.fontSize = 50;
                    labelAMChartTime.text = data.qi_time_2;
                    // labelAMChartTime.fill = am4core.color(data.qi_detail_info['bgColor']);
                    $('#box-2 .effect-health').html('');
                    $('#box-2 .effect-health').html(data.qi_detail_info['description']);
                    $('#box-2 .effect-health').css({'color': '#000'});
                    if (data.qi_value == "-") {
                        $('#box-2 #title-no-data-2').html("<h3>Không có dữ liệu</h3>");
                    } else {
                        $('#box-2 #title-no-data-2').html("");
                    }
                }
            },
        });


        // $('#block_stations_indicator').html('');
        url = siteUrl + '/services/call/json/qi_detail_24h';
        payload  = {
            station_id: station_id,
        };
        // Load data for block 1
        $.ajax({
            type: "POST",
            dataType: 'json',
            url: url,
            data: payload,
            async: true,
            processData: true,
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            enctype: 'multipart/form-data',
            success: function(data){
                if (data.success){
                    var row = '';
                    var myObj = data.res,
                        keys = Object.keys(myObj),
                        i, len = keys.length;
                    keys.sort();
                    var lengthData = 0;
                    var qi_time_3 = data['qi_time_3'];

                    for (i = 0; i < len; i++) {
                        k = keys[i];
                        var sparklinesClass = 'sparklines sparklines-' + k;
                        var box3Sparklines = '#box-3 .sparklines-' + k;
                         if (lengthData == 0) {
                            lengthData = myObj[k]['values'].length;
                        }
                        var dataConvert = createTimeLookupsAQIChart(myObj[k]['values']);

                        if (["PM-10", "PM-2-5"].includes(k)) {
                            kText = k;
                            if (k == "PM-2-5") {
                                kText = "PM-2.5";
                            }

                            if (true) {
                                var tr = '<tr>';
                                tr += '<td>' + kText + '</td>';
                                tr += '<td>' + Math.round(myObj[k]['current']) + '</td>';
                                tr += '<td><span class="' + sparklinesClass + '" ' + 'sparkHeight="24px" sparkBarWidth="' + sparkBarWidthValue +  '" sparkChartRangeMin="0" sparkType="bar" >' + dataConvert['dataValues'].join(',')  + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['min']) + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['max']) + '</span></td>';
                                tr += '</tr>';
                                $('#box-3 .table-chart tbody').append(tr);
                            }

                            $(box3Sparklines).sparkline('html', {
                                enableTagOptions: true,
                                colorMap: data.color_map,
                                tooltipFormat: "VN AQI: {{value:val}} ,  {{offset:timeLookup}}",
                                tooltipValueLookups: {
                                    "val": {"-1": "N/A"},
                                    "timeLookup": dataConvert['dataTimes'],
                                }
                            });

                        }
                    }

                    for (i = 0; i < len; i++) {
                        k = keys[i];
                        var sparklinesClass = 'sparklines sparklines-' + k;
                        var box3Sparklines = '#box-3 .sparklines-' + k;
                        var dataConvert = createTimeLookupsAQIChart(myObj[k]['values']);

                        if (!["PM-10", "PM-2-5"].includes(k)) {
                            if (true) {
                                var tr = '<tr>';
                                tr += '<td>' + k + '</td>';
                                tr += '<td>' +Math.round(myObj[k]['current']) + '</td>';
                                tr += '<td><span class="' + sparklinesClass + '"  ' + 'sparkHeight="24px" sparkBarWidth="' + sparkBarWidthValue +  '" sparkChartRangeMin="0" sparkType="bar" >' +dataConvert['dataValues'].join(',')  + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['min']) + '</span></td>';
                                tr += '<td><span class="num-blue">' + Math.round(myObj[k]['max']) + '</span></td>';
                                tr += '</tr>';
                                $('#box-3 .table-chart tbody').append(tr);
                            }

                           $(box3Sparklines).sparkline('html', {
                                enableTagOptions: true,
                                colorMap: data.color_map,
                                tooltipFormat: "VN AQI: {{value:val}} ,  {{offset:timeLookup}}",
                                tooltipValueLookups: {
                                    "val": {"-1": "N/A"},
                                    "timeLookup": dataConvert['dataTimes'],
                                }
                            });
                        }
                    }

                     // Display start date - end date chart
                    $('#start_date_aqi_24h').empty();
                    $('#end_date_aqi_24h').empty();
                    $('#mid_date_aqi_24h').empty();
                    $('#start_date_aqi_24h').append(data['min_date']);
                    $('#end_date_aqi_24h').append(data['max_date']);
                    // $('#mid_date_aqi_24h').append();

                    hand24h.showValue(Number(data.qi_value), am4core.ease.cubicOut);
                    $('#name_tram_24h').html("VN_AQI Ngày: " + data.station_name);
                    labelAMChart24h.text = data.qi_value;
                    labelAMChart24h.fill = am4core.color('#000');
                    labelAMChart24h.fontSize = 50;
                    labelAMChartTime24h.text = data.qi_time_2;
                    $('#box-3 .effect-health').html('');
                    $('#box-3 .effect-health').html(data.qi_detail_info['description']);
                    $('#box-3 .effect-health').css({'color': '#000'});
                    if (data.qi_value == "-") {
                        $('#box-3 #title-no-data-3').html("<h3>Không có dữ liệu</h3>");
                    } else {
                        $('#box-3 #title-no-data-3').html("");
                    }
                }
            },
        });
    }
}

function loadDataTableForPage() {
    // For 30day
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '2%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
    ];

    var aoClass = ['', '', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });

    return true;
}

function loadDataTableForPage_24h() {
    // For 24h
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [
        {'sWidth' : '2%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
    ];

    var aoClass = ['', '', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable : 1,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "station_id", "value": $('#cbbStations').val(),
            });
        },
    });

    return true;
}

function loadDataTableForPageWater_1() {
    // For 24h
    var sAjaxSource = $("#custom_datatable_2").attr("data-url");
    var aoColumns = [
        {'sWidth' : '2%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
    ];

    var aoClass = ['', '', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable : 2,
        iDisplayLength: 5,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "station_id", "value": $('#cbbStations').val(),
            });
        },
    });

    return true;
}

//create Time Lookups AQI Chart
function createTimeLookupsAQIChart(dataAqi) {
    var dataValues = new Array();
    var dataTimes = new Array();
    if (!dataAqi || dataAqi.length === 0) {
        return {'dataValues': dataValues, dataTimes: dataTimes};
    }
    var lengthData = dataAqi.length;
    for (var i = 0; i < lengthData; i++) {
        var dataAqi_i = dataAqi[i];
        for (var dataValue in dataAqi_i) {
            dataValues.push(dataValue);
            var dateStrFromat = dataAqi_i[dataValue].split(" ");
            var dateFromat = dateStrFromat[1] + ' ' + dateStrFromat[0];
            dataTimes.push(dateFromat);
        }
    }
    return {'dataValues': dataValues.reverse(), dataTimes: dataTimes.reverse()};
}

function startEndTimeChart(lengthData, qi_time_2, isHours) {

    var dateStrFromat = qi_time_2.split(" ");
    var dateFromat = new Date(dateStrFromat[0].replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$2/$1/$3") + ' ' + dateStrFromat[1] + ':00');
    dateFromat.setHours(dateFromat.getHours() - lengthData);
    var month = '' + (dateFromat.getMonth() + 1),
            day = '' + dateFromat.getDate(),
            hours = dateFromat.getHours();
    if (month.length < 2) {
        month = '0' + month;
    }
    if (day.length < 2) {
        day = '0' + day;
    }
    if (isHours) {
        return hours + ':00 ';
    }
    return [day, month].join('/') + ' ' + hours + ':00';
}

function loadDataTableListStations() {
    var sAjaxSource = $("#custom_datatable_3").attr("data-url");
    var aoColumns = [
        {'sWidth' : '10%'},
        {'sWidth' : '40%'},
        {'sWidth' : '50%'},
    ];

    var aoClass = ['', 'text-left', 'text-left'];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable : 3,
        iDisplayLength: 10,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "station_type", "value": $('#cbbStationType').val(),
            });
            aoData.push({
                "name": "province_id", "value": $('#panelSearchProvinces').val(),
            });
        },
    });

    return true;
}

function loadDataProvinceHaveStations(currentId) {
        var url = $("#hfURLLoadProvinceHaveStation").val();

        var data = {
            station_type: currentId,
            from_public: 1,
        };
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $('#panelSearchProvinces').html(res.html);
                    $('#panelSearchProvinces').trigger("chosen:updated");
                }
            }
        });

        return true;
}

function checkIfExistStation(station_id) {
    for(var i=0; i<loaded_stations.length; i++){
        if (loaded_stations[i]['station_id'] == station_id){
            return true;
        }
    }
    return false;
}


function getStationInBackground(station_id, callback) {
    if (typeof callback == 'function'){console.log('getStationInBackground2');
        callback();
    }
    return true;
}
function exportMap() {
    var link = document.getElementById('image-download');
    html2canvas(document.querySelector("#map")).then(canvas => {
      link.href = canvas.toDataURL();
      console.log(link.href)
      link.click();
  });
}

