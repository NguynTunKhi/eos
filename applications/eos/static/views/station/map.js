// Global variables for page
var map = null;
var json_station_status = null;
var json_indicators = null;
var json_area = null;
var json_provinces = null;
var loaded_stations = [];

$(document).ready(function(){
    // Initialize value for global variables
    if (true) {
        json_station_status = $('#json_station_status').html();
        json_station_status = JSON.parse(json_station_status);
        json_indicators = $('#json_indicators').html();
        json_indicators = JSON.parse(json_indicators);
        json_area = $('#json_area').html();
        json_area = JSON.parse(json_area);
        json_provinces = $('#json_provinces').html();
        json_provinces = JSON.parse(json_provinces);
    }

    // Add 'Warning level' and 'Toolbar' on Map
    var addCustomFuncitonToMapInterval = setInterval(function () {
        var panelTieuChuan = $("#map>div").find(".panelTieuChuan");
        if (panelTieuChuan.length != 0) {
            clearInterval(addCustomFuncitonToMapInterval);
        } else {
            var html =
                "<div class='panelTieuChuan'>" +
                "<h4>" + app.translate('Warning Levels') + "</h4>";
            for (var key in json_station_status) {
                html += "<div data-id='" + key + "' title='" + json_station_status[key].name + "'>" +
                    "<i style='background-color:" + json_station_status[key].color + "'></i><span>" + json_station_status[key].name +
                    "</span></div>";
            }
            html += "</div>" +
                "<div class='panelControl'>" +
                "<span></span>" +
                "<label><input class='chkShowHideLabel' type='checkbox' checked>" + app.translate('Show labels') + "</label>" +
                "<div class='toolParameters'>" + app.translate('Indicators') + "<i class='fa fa-arrow-down'></i>" +
                "<div class='items' style='display: none'>";
            for (var key in json_indicators) {
                if (json_indicators.hasOwnProperty(key)) {
                    html += "<div class='item' data-type='" + json_indicators[key].indicator_type + "' data-id='" + key + "'><label><input type='checkbox'>" + json_indicators[key].indicator + "</label></div>";
                }
            }
            html += "</div>" +
                "</div>"+
            "</div>";
            $("#map>div").append(html);
        }
    }, 300);

    // Show timer on Map
	var showClockOnMapInterval = setInterval(function(){
        var currentTime = new Date();
        var hours = currentTime.getHours();
        var minutes = currentTime.getMinutes();
        var seconds = currentTime.getSeconds();
        var displayTime = app.formatTime(hours, minutes, seconds);
		$(".panelControl>span").html(displayTime);
	}, 1000);

	// Register all events for this page
    if (true) {
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
            if ($(this).prop('checked')) {
                $('.mapLabel').show();
            } else {
                $('.mapLabel').hide();
            }
        });

        $('body').on('click', '.toolParameters .item input', function (e) {
            showHideIndicatorForStation();
        });

        $('body').on('click', '.mapLabel h4', function (e) {
            var parent = $(this).closest('.mapLabel');
            parent.find('p').hide();
            var id = parent.data('id');
            getStationInBackground(id, function () {
                $('.mapMarker[data-id=' + id + ']').trigger('click', [true]);
            });
        });

        $('body').on('click', '.ibox-content.change-type .ibox .ibox-content .item', function (e) {
            var lat = $(this).data('lat');
            var lon = $(this).data('lon');
            var id = $(this).data('id');
            getStationInBackground(id, function () {
                var marker2 = $('.mapMarker[data-id=' + id + ']');
                map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
                marker2.trigger('click', [true]);
            });
        });

        $('body').on('click', '.btnChangeOption', function (e) {
            if ($(this).hasClass('active')) {
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
            if ($(this).hasClass('active')) {
                return false;
            }
            $('.btnChangeType').removeClass('active');
            $(this).addClass('active');
            var name = $(this).text();
            $('.change-type-title').html(name);
            var type = $(this).data('type');
            if (!type) {
                $('.change-type').find('.ibox').show();
            } else {
                $('.change-type').find('.ibox').hide();
                $('.change-type').find('.ibox[data-type=' + type + ']').show();
            }
        });

        $('body').on('click', '.block-status', function (e) {
            var checked = true;
            var colors = ['#1dce6c', '#F1D748', '#F08432', '#EA3223', '#999999', 'purple']
            var status = $(this).data('status');

            if ($(this).hasClass('active')) {
                checked = false;
                $(this).removeClass('active');
                $(this).css('background', '');
                $(this).css('color', '#000');
            } else {
                $(this).addClass('active');
                $(this).css('background', colors[status]);
                $(this).css('color', '#fff');
            }
            var mapMarker = $('.mapMarker[data-status=' + status + ']');
            var mapLabel = $('.mapLabel[data-status=' + status + ']');
            if (checked) {
                mapMarker.show();
            } else {
                mapMarker.hide();
            }
            if ($('.chkShowHideLabel').prop('checked')) {
                if (checked) {
                    mapLabel.show();
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

        $('body').on('change', '#cbbStationTypePanel', function (e) {
            var url = $(this).data('url');
            var station_type = $(this).val();
            if (station_type){
                showHideMarker($('.mapMarker[data-station_type="' + station_type + '"]'));
            } else {
                showHideMarker($('.mapMarker'));
            }
            var data = {
                station_type: station_type
            };
            app.postAjax({
                url: url,
                data: data,
                callback: function (res) {
                    if (res.success) {
                        $('#cbbStations').html(res.html);
                        $('#cbbStations').trigger("chosen:updated");
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

        $('body').on('change', '#panelSearchArea', function (e) {
            var url = $(this).data('url');
            var area_id = $(this).val();
            if (area_id){
                showHideMarker($('.mapMarker[data-area_id="' + area_id + '"]'));
            } else {
                showHideMarker($('.mapMarker'));
            }
            var data = {
                area_id: area_id
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
                                map.getView().setZoom(8);
                            } else {
                                map.getView().setZoom(5.5);
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
                showHideMarker($('.mapMarker[data-province_id="' + province_id + '"]'));
            } else {
                showHideMarker($('.mapMarker'));
            }
            var data = {
                province_id: province_id
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
                            if (province_id) {
                                map.getView().setZoom(8);
                            } else {
                                map.getView().setZoom(5.5);
                            }
                        }
                    }
                }
            });
        });

        $('body').on('change', '#cbbStations', function (e) {
            if ($(this).val()) {
                var selectedOption = $(this).find('option:selected');
                var lat = selectedOption.data('lat');
                var lon = selectedOption.data('lon');
                if (lat && lon) {
                    map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
                }
                var id = selectedOption.data('id');
                getStationInBackground(id, function () {
                    $('.mapMarker[data-id=' + id + ']').trigger('click', [true]);
                });
            }
        });

        $('body').on('click', '.mapMarker', function (e, fromLabel) {
            var currentId = $(e.target).data('id');
            if (e.originalEvent != undefined || fromLabel) {
                getStationInBackground(currentId, function () {
                    $('.mapMarker[data-id!=' + currentId + ']').closest('.ol-overlay-container').find('.popover').closest('.ol-overlay-container').find('.mapMarker').trigger('click');
                });
            }
            var urlHistorical = $('#hfUrlToHistoricalData').val();
            urlHistorical += '&' + $.param({station_id: currentId});
            if ($('.mapMarker[data-id=' + currentId + ']').closest('.ol-overlay-container').find('.view-more').length == 0) {
                var buttonHtml = '<a class="view-more" target="_blank" href="' + urlHistorical + '">' + app.translate('View more') + '</a>';
                buttonHtml += '<button type="button" class="close closePopover">&times;</button>';
                $('.mapMarker[data-id=' + currentId + ']').closest('.ol-overlay-container').find('.popover').find('.popover-title').append(buttonHtml);
            }
            $(".location-popover").not(this).popover('hide');

            showHideIndicatorForStation();
        });
    }

    // Initialize map
	initMap();

    // Add slimscroll to element
    $('.full-height-scroll').slimscroll({
        height: 'auto'
    });
    $('.fh-sidebar').slimscroll({
        height: '100%'
    });
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

function initMap() {
    map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Group({
                'title': 'Bản đồ',
                layers: [
                    new ol.layer.Tile({
                        title: 'VietBanDo',
                        visible: true,
                        type: 'base',
                        source: new ol.source.XYZ({
                              attributions: 'Copyright:© 2013 ESRI, i-cubed, GeoEye',
                              url:'https://map.hap-technology.com/ImageLoader/GetImage.ashx?Ver=2016&LayerIds=VBD&Level={z}&X={x}&Y={y}'
                        })
                    }),
                    // new ol.layer.Tile({
                    //     title: 'Map',
                    //     visible: false,
                    //     type: 'base',
                    //     source: new ol.source.BingMaps({
                    //         key: 'AhjZCP7OMYpOH4RkRtLfpDwGu8VkY_cA6Uqc0XU1Fves8DjkEyXrVgiP4I0T16rh',
                    //         imagerySet: 'Road'
                    //     })
                    // }),
                ]
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([105.80, 17.03]),
            zoom: 5.5
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
    map.addLayer(vectorLayer);

    var tooltip = document.getElementById('tooltip');
    var overlay = new ol.Overlay({
        element: tooltip,
        offset: [10, 0],
        positioning: 'bottom-left'
    });
    map.addOverlay(overlay);

    // Hoang Sa
    var pos = ol.proj.fromLonLat([112.839614, 16.248081]);

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

    var stationId = $('#hfFocusedStation').val();
    if (stationId){
        var lon = parseFloat($('#hfFocusedStation').data('longitude'));
        var lat = parseFloat($('#hfFocusedStation').data('latitude'));
        map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
        setTimeout(function () {
            getStationInBackground(stationId, function () {
                $('.mapMarker[data-id=' + stationId + ']').trigger('click');
            });
        }, 500);
    }

    // Load station into map in background
    getStationInBackground('');
}

function showHideIndicatorForStation() {
    var items = $('.toolParameters .item input');
    var total = items.length;
    for (var i = 0; i < total; i++) {
        var item = $(items[i]);
        var id = item.closest('.item').data('id');
        if (item.prop('checked')) {
            $('.mapLabel').find('.param[data-id=' + id + ']').show();
        } else {
            $('.mapLabel').find('.param[data-id=' + id + ']').hide();
        }
    }
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
    if (checkIfExistStation(station_id)){
        if (typeof callback == 'function'){
            callback();
        }
        return true;
    }
    var total_station = parseInt($("#hfTotalStation").val());
    var max_dsp = 100;
    var url = $("#map").attr("data-url");
    var dsp_start = $("#map").attr("data-dsp_start");
    if (!dsp_start){
        dsp_start = '0';
    }
    dsp_start = parseInt(dsp_start);
    if (station_id || (dsp_start < max_dsp - 1 && dsp_start <= total_station - 1)) {
        var data = {
            dsp_start: dsp_start,
            station_id: station_id,
        };
        if (station_id) {
            app.showProgress('#map');
        }
        app.postAjax({
            url: url,
            showProgress: false,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $("#map").attr("data-dsp_start", res.dsp_next);
                    var stations = res.data;
                    for (var key in stations) {
                        if (stations.hasOwnProperty(key)) {
                            var point = stations[key];
                            if (checkIfExistStation(point.station_id)){
                                continue;
                            }
                            loaded_stations.push(point);
                            var html =
                                "<div class='stationInfo' data-status='" + point.status + "' data-id='" + point.station_id + "'>" +
                                "<div><b>" + app.translate('Station Code:') + " </b> " + point.station_code + "</div>" +
                                "<div><b>" + app.translate('Province:') + " </b> " + point.province_name + "</div>" +
                                "<div><b>" + app.translate('Address:') + " </b> " + point.address + "</div>" +
                                "<div><b>" + app.translate('Latitude:') + " </b> " + point.lonlat[1] + " - <b>" + app.translate('Longitude') + "</b> " + point.lonlat[0] + "</div>" +
                                "<div><b>" + app.translate('Status:') + "</b> <b style='font-size: 1.2em; color: " + json_station_status[point.status]['color'] + "'>" + point.status_disp + "</b></div>" +
                                "<div id='table-wrapper'>" +
                                "  <div id='table-scroll'><table class='table table-striped table-bordered table-hover table-responsive dataTable no-footer'>" +
                                "<tr><th>#</th><th>" + app.translate('Parameter') + "</th><th>" + app.translate('Value') + "</th><th>" + app.translate('Unit') + "</th></tr>";
                            var totalParams = point.parameters.length;
                            for (var j = 0; j < totalParams; j++) {
                                var parameter = point.parameters[j];
                                if (parameter.cmax == null && parameter.cmin == null) {
                                    html += "<tr><td>" + (j + 1).toString() + "</td><td>" + parameter.key + "</td><td style='color: #fff; background: " + parameter.color + "'>" + parameter.value + "<br>" + "</td><td>" + parameter.unit + "</td></tr>";
                                }
                                else if (parameter.cmax == null) {
                                    html += "<tr><td>" + (j + 1).toString() + "</td><td>" + parameter.key + "</td><td style='color: #fff; background: " + parameter.color + "'>" + parameter.value + "<br>" + "<i class='cmin'>(" + "Cmin: " + parameter.cmin + ")</i></td><td>" + parameter.unit + "</td></tr>";
                                }
                                else if (parameter.cmin == null) {
                                    html += "<tr><td>" + (j + 1).toString() + "</td><td>" + parameter.key + "</td><td style='color: #fff; background: " + parameter.color + "'>" + parameter.value + "<br>" + "<i class='cmax'>(" + "Cmax: " + parameter.cmax + ")</i></td><td>" + parameter.unit + "</td></tr>";
                                }
                                else {
                                    html += "<tr><td>" + (j + 1).toString() + "</td><td>" + parameter.key + "</td><td style='color: #fff; background: " + parameter.color + "'>" + parameter.value + "<br>" + "<i class='cmax'>(" + "Cmax: " + parameter.cmax + "</i><i class='cmin'>" + ", Cmin: " + parameter.cmin + ")</i></td><td>" + parameter.unit + "</td></tr>";
                                }
                            }
                            html +=
                                "</table></div></div>" +
                                "</div>";
                            var pos = ol.proj.fromLonLat(point.lonlat);
                            var selector_id = 'marker_' + point.station_id;
                            var selector = '<div id="' + point.station_id + '" class="mapMarker" data-status="' + point.status + '" data-id="' + point.station_id + '" title="' + point.station_name + '"'+
                                ' style="background-color: ' + json_station_status[point.status]['color'] + '"'+
                                ' data-station_type="' + point.station_type + '" data-province_id="' + point.province_id + '"'+
                                ' data-area_id="' + point.area_id + '">';
                            // point
                            var marker = new ol.Overlay({
                                position: pos,
                                positioning: 'center-center',
                                // element: document.getElementById(selector_id),
                                element: $(selector).popover({
                                    'placement': 'left',
                                    'html': true,
                                    'content': html,
                                })[0],
                                stopEvent: false
                            });
                            map.addOverlay(marker);

                            // label
                            html = "<h4>" + point.station_name + "</h4>";
                            for (var j = 0; j < totalParams; j++) {
                                var parameter = point.parameters[j];
                                html += "<p class='param' style='display: none; color: #fff; background-color: " + parameter.color + "' data-id='" + parameter['id'] + "'>" + parameter['key'] + ": " + parameter['value'] + " " + parameter['unit'] + "</p>";
                            }
                            var label = new ol.Overlay({
                                position: pos,
                                element: $("<div id='mapLabel' data-status='" + point.status + "' data-id='" + point.station_id + "' class='mapLabel'>").html(html)[0],
                                stopEvent: false,
                            });
                            map.addOverlay(label);
                        }
                    }

                    if (typeof callback == 'function'){
                        callback();
                    }
                }
                getStationInBackground();
                if (station_id) {
                    app.hideProgress('#map');
                }
            }
        });
    }
}