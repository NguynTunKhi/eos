$(document).ready(function(){

    loadDataTableForPage();
    loadDataTableForPage2();

    $("body").on("change", "#cbbTramNuocThai, #cbbTramKhiThai", function () {
        var stationId  = $(this).val();
        var url = $(this).data('url');
        var currentSelector = $(this).attr('id');
        if (stationId){
            app.postAjax({
                url: url,
                data: {stationId: stationId},
                callback: function (res) {
                    if (currentSelector == 'cbbTramNuocThai'){
                        container = '#sliderNuocThai';
                    } else {
                        container = '#sliderKhiThai';
                    }
                    createChartTramNuocThai(container, res.charts);
                }
            });
        }
    });

    $('#cbbTramNuocThai, #cbbTramKhiThai').trigger("change");
});

function loadDataTableForPage() {
    if (typeof loadDataTable == "function"){
        var sAjaxSource = $("#custom_datatable_0").attr("data-url");
        var aoColumns = [
                        { "sWidth": "5%", "bSortable": false },
                        { "sWidth": "45%" },
                        { "sWidth": "45%" },
                        ];
        var sDom = "<'row middle't><'clear'>";
        var aoClass = ['', 'text-left', 'text-left'];
        loadDataTable({
            sAjaxSource: sAjaxSource,
            aoColumns: aoColumns,
            aoClass: aoClass,
            sDom: sDom,
        });
    } else {
        setTimeout(loadDataTableForPage, 30);
    }
}

function loadDataTableForPage2() {
    if (typeof loadDataTable == "function"){
        var sAjaxSource = $("#custom_datatable_2").attr("data-url");
        var aoColumns = [
                        { "sWidth": "10%", "bSortable": false },
                        { "sWidth": "45%" },
                        { "sWidth": "45%" },
                        ];

        var aoClass = ['', 'text-left', 'text-left'];
        var sDom = "<'row middle't><'clear'>";
        loadDataTable({
            sAjaxSource: sAjaxSource,
            aoColumns: aoColumns,
            aoClass: aoClass,
            iTable: 2,
            sDom: sDom,
        });
    } else {
        setTimeout(loadDataTableForPage2, 30);
    }
}

function createChartTramNuocThai(container, charts) {
    var carousel_indicators = "<ol class='carousel-indicators'>";
    var carousel_inner = "<div class=\"carousel-inner\">";
    var idx = 0;
    for (var key in charts) {
        if (!charts.hasOwnProperty(key)) {continue;}
        if (idx == 0) {
            carousel_indicators += "<li data-target='#" + key + "' data-slide-to='" + idx + "' class='active'></li>";
            carousel_inner += "<div id='" + key +  "' class='item active'></div>";
        } else {
            carousel_indicators += "<li data-target='#" + key + "' data-slide-to='" + idx + "'></li>";
            carousel_inner += "<div id='" + key +  "' class='item'></div>";
        }
        idx += 1;
    }
    carousel_indicators += "</ol>";
    carousel_inner += "</div>";
    var next_privious = "<a class='left carousel-control' href='" + container + "' data-slide='prev'>" +
        "<span class='glyphicon glyphicon-chevron-left'></span>" +
        "<span class='sr-only'>Previous</span>" +
        "</a>" +
        "<a class='right carousel-control' href='" + container + "' data-slide='next'>" +
        "<span class='glyphicon glyphicon-chevron-right'></span>" +
        "<span class='sr-only'>Next</span>" +
        "</a>";
    $(container).html(carousel_indicators + carousel_inner + next_privious);
    $(container).carousel();
    for (var key in charts) {
        if (!charts.hasOwnProperty(key)) {
            continue;
        }
        Highcharts.chart(key, {
            chart: {
                type: 'line',
                zoomType: 'x'
            },
            title: charts[key].title,
            subtitle: charts[key].subtitle,
            xAxis: charts[key].xAxis,
            credits: {
                enabled: false
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: false
                    },
                    enableMouseTracking: true
                }
            },
            series: charts[key].series

        });
    }
}