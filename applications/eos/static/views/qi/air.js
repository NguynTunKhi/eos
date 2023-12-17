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
        bg: '#008000',
        color: '#ffffff',
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
    // Add slimscroll to element
    $('.fh-sidebar').slimscroll({
        height: '100%'
    });
    
    json_station_status = $('#json_station_status').html();
    json_station_status = JSON.parse(json_station_status);
    json_indicators = $('#json_indicators').html();
    json_indicators = JSON.parse(json_indicators);
    json_stations = $('#json_stations').html();
    json_stations = JSON.parse(json_stations);
    json_area = $('#json_area').html();
    json_area = JSON.parse(json_area);
    json_provinces = $('#json_provinces').html();
    json_provinces = JSON.parse(json_provinces);
    indexItems = $('#json_index_items').html();
    indexItems = JSON.parse(indexItems);
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
                "<span></span>" +
                "<label><input class='chkShowHideLabel' type='checkbox'>" + app.translate('Show labels') + "</label>" ;
             html +=
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
            $('.mapLabel').show();
        } else {
	        $('.mapLabel').hide();
        }
    });

	$(window).ready(function () {
	    if ($('.chkShowHideLabel').prop('checked')){
                $('.mapLabel').show();
            } else {
                $('.mapLabel').hide();
            }
    });



/*
if(document.getElementsByClassName('chkShowHideLabel').checked) {
    console.log('checked');
     $('.mapLabel').show();
} else {
    console.log('unchecked');
      $('.mapLabel').hide();
}
*/


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

	$('body').on('click', '.ibox-content.change-type .ibox .ibox-content .item', function (e) {
	    var lat = $(this).data('lat');
	    var lon = $(this).data('lon');
	    map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
        var id = $(this).data('id');
        $('.mapMarker[data-id=' + id + ']').trigger('click', [true]);
    });

	$('body').on('change', '#cbbStations', function (e) {
	    var selectedOption = $(this).find('option:selected');
	    var lat = selectedOption.data('lat');
	    var lon = selectedOption.data('lon');
	    map.getView().setCenter(ol.proj.fromLonLat([lon, lat]));
        var id = selectedOption.data('id');
        $('.mapMarker[data-id=' + id + ']').trigger('click', [true]);
        // Show chart on left bar
        var stationId  = $('#cbbStations').val();
        createChartForAQIIndicators(stationId);
    });

	initMap();
	
    // Add slimscroll to element
    $('.full-height-scroll').slimscroll({
        height: 'auto'
    });

    $('.i-checks').iCheck({
        checkboxClass: 'icheckbox_square-green',
        radioClass: 'iradio_square-green',
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
                            map.getView().setZoom(7);
                        } else {
                            map.getView().setZoom(5.5);
                        }

                        for (var key in json_stations) {
                            if (json_stations.hasOwnProperty(key)) {
                                var point = json_stations[key];
                                var html =
                                    "<div class=\"modal-dialog modal-md\">" +
                                    "<div class=\"modal-content\">" +
                                    "<div class=\"modal-header\">" +
                                    "<button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button>" +
                                    "<h4 class=\"modal-title\">Sumary info</h4>" +
                                    "</div>" +
                                    "<div class=\"modal-body\">" +
                                    "<div class=\"row\"><div class=\"col-sm-4 custom-index\" style=\"background-color: " +
                                        point.bgColor + "; color: " + point.Color  + "\">" + point.index +
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
                                var contentPopover = app.translate('Index') + ": <span class=\"custom-index-popover\" style=\"background-color: " +point.bgColor +
                                    "; color: " + point.Color + "\">" + point.index + "</span><br />";
                                if (point.qi_time3) {
                                    contentPopover += "<div class=\"text-center\">" + point.qi_time3 + "<br><i>(" + point.qi_time2 + ")</i></div>";
                                }
                                contentPopover += "<hr style=\"margin: 10px 0px 0px\"><div class=\"text-center\"><i>" + app.translate('click for more information') + "</i></div>";
                                var selector = "<div class='mapMarker' data-status='" + point.status + "' data-id='" + point.station_id + "' title='" + point.station_name + "'"+
                                    " style='background-color: " + point.bgColor + "; color: " + point.Color  + "'" +
                                    ' data-station_type="' + point.station_type + '" data-province_id="' + point.province_id + '"'+
                                    ' data-area_id="' + point.area_id + '" ' +
                                    " data-content='" + html + "'>" + point.index + "</div>";
                                // point
                                var marker = new ol.Overlay({
                                    position: pos,
                                    positioning: 'center-center',
                                    // element: document.getElementById('marker'),
                                    element: $(selector).on('click', function (e, fromLabel) {
                                        var station_id = $(this).data('id');

                                        var content = $(this).data('content');

                                        // Call action to redraw right panel
                                        var url = $('#hfUrlLoadAQI').val();
                                        $(".my-modal .modal-body").load(url, {station_id: station_id} , function(){
                                            $('.my-modal').modal();
                                            var colorMap = $('.hf_color_map').html();
                                            colorMap = JSON.parse(colorMap);
                                            $('.sparklines').sparkline('html', { enableTagOptions: true, colorMap: colorMap });
                                        });

                                        // Show chart on left bar
                                        createChartForAQIIndicators(station_id);
                                        createChartForeachIndicators(station_id);
                                    })[0],
                                    stopEvent: false
                                });
                                map.addOverlay(marker);
                            }
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

                        for (var key in json_stations) {
                            if (json_stations.hasOwnProperty(key)) {
                                var point = json_stations[key];
                                var html =
                                    "<div class=\"modal-dialog modal-md\">" +
                                    "<div class=\"modal-content\">" +
                                    "<div class=\"modal-header\">" +
                                    "<button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button>" +
                                    "<h4 class=\"modal-title\">Sumary info</h4>" +
                                    "</div>" +
                                    "<div class=\"modal-body\">" +
                                    "<div class=\"row\"><div class=\"col-sm-4 custom-index\" style=\"background-color: " +
                                        point.bgColor + "; color: " + point.Color  + "\">" + point.index +
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
                                var contentPopover = app.translate('Index') + ": <span class=\"custom-index-popover\" style=\"background-color: " +point.bgColor +
                                    "; color: " + point.Color + "\">" + point.index + "</span><br />";
                                if (point.qi_time3) {
                                    contentPopover += "<div class=\"text-center\">" + point.qi_time3 + "<br><i>(" + point.qi_time2 + ")</i></div>";
                                }
                                contentPopover += "<hr style=\"margin: 10px 0px 0px\"><div class=\"text-center\"><i>" + app.translate('click for more information') + "</i></div>";
                                var selector = "<div class='mapMarker' data-status='" + point.status + "' data-id='" + point.station_id + "' title='" + point.station_name + "'"+
                                    " style='background-color: " + point.bgColor + "; color: " + point.Color  + "'" +
                                    ' data-station_type="' + point.station_type + '" data-province_id="' + point.province_id + '"'+
                                    ' data-area_id="' + point.area_id + '" ' +
                                    " data-content='" + html + "'>" + point.index + "</div>";
                                // point
                                var marker = new ol.Overlay({
                                    position: pos,
                                    positioning: 'center-center',
                                    // element: document.getElementById('marker'),
                                    element: $(selector).on('click', function (e, fromLabel) {
                                        var station_id = $(this).data('id');

                                        var content = $(this).data('content');

                                        // Call action to redraw right panel
                                        var url = $('#hfUrlLoadAQI').val();
                                        $(".my-modal .modal-body").load(url, {station_id: station_id} , function(){
                                            $('.my-modal').modal();
                                            var colorMap = $('.hf_color_map').html();
                                            colorMap = JSON.parse(colorMap);
                                            $('.sparklines').sparkline('html', { enableTagOptions: true, colorMap: colorMap });
                                        });

                                        // Show chart on left bar
                                        createChartForAQIIndicators(station_id);
                                        createChartForeachIndicators(station_id);
                                    })[0],
                                    stopEvent: false
                                });
                                map.addOverlay(marker);
                            }
                        }
                    }
                }
            }
        });
    });

    // Show chart on left bar
    var stationId  = $('#cbbStations').val();
    createChartForeachIndicators(stationId);
    createChartForAQIIndicators(stationId);
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

function initMap() {
    map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Group({
                'title': 'Base maps',
                layers: [
                    // new ol.layer.Tile({
                    //     title: 'Map',
                    //     type: 'base',
                    //     visible: true,
                    //     source: new ol.source.OSM()
                    // }),
//                    new ol.layer.Tile({
//                        title: 'Statellite',
//                        visible: false,
//                        type: 'base',
//                        source: new ol.source.TileJSON({
//                          //  url: 'https://api.tiles.mapbox.com/v3/mapbox.natural-earth-hypso-bathy.json?secure',
//                            url: 'http://api.tiles.mapbox.com/v3/mapbox.geography-class.jsonp',
//                            crossOrigin: 'anonymous'
//                        })
//                    }),
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

    for (var key in json_stations) {
        if (json_stations.hasOwnProperty(key)) {
            var point = json_stations[key];
            var html =
                "<div class=\"modal-dialog modal-md\">" +
                "<div class=\"modal-content\">" +
                "<div class=\"modal-header\">" +
                "<button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button>" +
                "<h4 class=\"modal-title\">Sumary info</h4>" +
                "</div>" +
                "<div class=\"modal-body\">" +
                "<div class=\"row\"><div class=\"col-sm-4 custom-index\" style=\"background-color: " +
                    point.bgColor + "; color: " + point.Color  + "\">" + point.index +
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
            var contentPopover = app.translate('Index') + ": <span class=\"custom-index-popover\" style=\"background-color: " +point.bgColor +
                "; color: " + point.Color + "\">" + point.index + "</span><br />";
            if (point.qi_time3) {
                contentPopover += "<div class=\"text-center\">" + point.qi_time3 + "<br><i>(" + point.qi_time2 + ")</i></div>";
            }
            contentPopover += "<hr style=\"margin: 10px 0px 0px\"><div class=\"text-center\"><i>" + app.translate('click for more information') + "</i></div>";
            var selector = "<div class='mapMarker' data-status='" + point.status + "' data-id='" + point.station_id + "' title='" + point.station_name + "'"+
                " style='background-color: " + point.bgColor + "; color: " + point.Color  + "'" +
                ' data-station_type="' + point.station_type + '" data-province_id="' + point.province_id + '"'+
                ' data-area_id="' + point.area_id + '" ' +
                " data-content='" + html + "'>" + point.index + "</div>";
            // point
            var marker = new ol.Overlay({
                position: pos,
                positioning: 'center-center',
                // element: document.getElementById('marker'),
                element: $(selector).on('click', function (e, fromLabel) {
                    var station_id = $(this).data('id');

                    var content = $(this).data('content');

                    // Call action to redraw right panel
                    var url = $('#hfUrlLoadAQI').val();
                    $(".my-modal .modal-body").load(url, {station_id: station_id} , function(){
                        $('.my-modal').modal();
                        var colorMap = $('.hf_color_map').html();
                        colorMap = JSON.parse(colorMap);

                        var indicators = $('.hf_indicators').html();
                        indicators = JSON.parse(indicators);

                        var myObj = indicators,
                            keys = Object.keys(myObj),
                            i, len = keys.length;
                        keys.sort();
                        var lengthData = 0;
                        for (i = 0; i < len; i++) {
                            k = keys[i];
                            var sparklinesClass = 'sparklines sparklines-' + k;
                            var box2Sparklines = '.sparklines-' + k;
                            if (lengthData == 0) {
                                lengthData = myObj[k]['values_hf'].length;
                            }
                            var dataConvert = createTimeLookupsAQIChart(myObj[k]['values_hf']);

                            $(box2Sparklines).sparkline('html', {
                                enableTagOptions: true,
                                colorMap: colorMap,
                                tooltipFormat: "VN AQI: " + "{{value:val}} ,  {{offset:timeLookup}}",
                                tooltipValueLookups: {
                                    "val": {"-1": "N/A"},
                                    "timeLookup": dataConvert['dataTimes'],
                                }
                            });
                        }
                        // $('.sparklines').sparkline('html', { enableTagOptions: true, colorMap: colorMap });
                    });

                    // Show chart on left bar
                    createChartForAQIIndicators(station_id);
                    createChartForeachIndicators(station_id);
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
                element: $("<div id='mapLabel' data-status='" + point.status + "' data-id='" + point.station_id + "' class='mapLabel'>").html(html)[0],
                stopEvent: false,
            });
            map.addOverlay(label);
        }
    }

    var template = '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-title"></div>' +
        '<div class="popover-content" style="min-width: 50px;"></div></div>';
    $(".custom-popover").popover({
        animation : true,
        placement: 'auto bottom',
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

}

function showHideIndicatorsBar(){
    var stationType = $('#cbbStationType').val();
    $('.toolParameters').find('.item').hide();
    $('.toolParameters').find('.item[data-type="' + stationType + '"]').show();
}

function createChartForeachIndicators(station_id) {
    var url = $('#hfUrlGetChartForStation').val();
    app.postAjax({
        showProgress: false,
        url: url,
        data: {station_id: station_id},
        callback: function (res) {
            var charts = res.charts;
            var res = res.res;
            $('.station_name_detail').html(res.station_name);
            $('.last_check_detail').html(res.last_check);
            $('.all-charts').html('');

            for (var k in res) {
                var html = '<div class="flot-chart-content" id="flot-bar-chart-' + k + '"></div>';
                $('.all-charts').append(html);
                // Create the COLUMNE chart
                var series_data = charts[k];
                var subtitle = '';
                Highcharts.chart('flot-bar-chart-' + k, {
                    chart: {
                        type: 'column',
                        backgroundColor: '#f3f3f4'
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

function createChartForAQIIndicators(stationId) {
    var url = $('#detailChartWidgetAqi').data('url');
    app.postAjax({
        showProgress: false,
        url: url,
        data: {station_id: stationId},
        callback: function (res) {
            $('.widget_aqi_info .indicator-value').html(res.aqi)
            $('.widget_aqi_info .at-time').html(res.at_time)
            $('.widget_aqi_info .at-date').html(res.at_date)
            var chart = res.chart;
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
                    data: chart.series[0].data
                }]
            });
        }
    });
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