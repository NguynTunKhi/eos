
function init_graph_detail() {
    var graphDetailInterval = setInterval(function (e) {
        if (typeof jQuery != 'function' || typeof Highcharts != 'object') {
            return false;
        }
        clearInterval(graphDetailInterval);
        // if (window.register_events_for_graph_detail) {
        //     return true;
        // }
        // window.register_events_for_graph_detail = 1;
        $(document).ready(function () {
            createChartForStationForAll();

            $('body').off('click', 'ul.nav.nav-tabs.load_import_graph_detail li');
            $('body').on('click', 'ul.nav.nav-tabs.load_import_graph_detail li', function (e) {
                if ($(this).hasClass('active')) {
                    return true;
                }
                if ($(this).hasClass('all')) {
                    $('.graph_detail_adjust_data').hide();
                    createChartForStationForAll();
                    return true;
                }
                var indicatorId = $(this).data('indicator');
                createChartForStationForItem(indicatorId);
            });

            // Khi view mode thay doi : minute/hour/day/month
            $('body').off('change', "#cbbShowBy");
            $('body').on('change', "#cbbShowBy", function () {
                var indicatorId = $('#hfIndicator').val();
                if (indicatorId == 'all') {
                    createChartForStationForAll();
                } else {
                    createChartForStationForItem(indicatorId);
                }
            });

            // Khi view mode thay doi : 1/7/15 days
            $('body').off('change', "#cbbDuration");
            $('body').on('change', "#cbbDuration", function () {
                var indicatorId = $('#hfIndicator').val();
                if (indicatorId == 'all') {
                    createChartForStationForAll();
                } else {
                    createChartForStationForItem(indicatorId);
                }
            });

            if ($('[id*="wbst-tab-"]').length > 0) {
                // Neu graph_detail nam trong 'widget_by_station_type'
                var container = $('[id*="wbst-tab-"].active');
                container.off('change', '[id*=cbbShowBy]');
                container.on('change', '[id*=cbbShowBy]', function () {
                    var indicatorId = $('#hfIndicator').val();
                    if (indicatorId == 'all') {
                        createChartForStationForAll();
                    } else {
                        createChartForStationForItem(indicatorId);
                    }
                });
            }

            // Khi view mode thay doi ngay start display
            $('body').off('click', '.btnStationTypeGo')
            $('body').on('click', '.btnStationTypeGo', function (e) {
                var indicatorId = $('#hfIndicator').val();
                if (indicatorId == 'all') {
                    createChartForStationForAll();
                } else {
                    createChartForStationForItem(indicatorId);
                }
            });

            // Khi click tab chart detail cua Indicator, luu indicator_id
            $('body').on('click', 'a[data-toggle="tab"]', function (e) {
                var target = $(e.target).attr("href"); // activated tab

                // Ko xu ly trong truong hop man hinh Dashboar, cac tab Station type dc click
                if (target.indexOf('wbst') != -1) return true;

                // Neu ko phai la tab All thi lay indicatior_id luu vao bien hfIndicator
                if (!target.includes('all')) {
                    $('#hfIndicator').val(target.substring(5));
                } else {
                    $('#hfIndicator').val('all');
                }
            });
        });
    }, 50);
}

init_graph_detail();

function graph_detail_reload_chart() {
    createChartForStationForItem($('#hfIndicator').val());
}

function createChartForStationForAll(container) {
    if (container == undefined){
        container = $('body');
    }
    if ($('[id*="wbst-tab-"]').length > 0){
        // Neu graph_detail nam trong 'widget_by_station_type'
        container = $('[id*="wbst-tab-"].active').find('.widget_graph_detail');
    }
    var stationId  = container.find('#hfStationId').val();
    var url = $('#hfUrlGetChart').val();
    var chartStart = $("#chartStart").val();
    var chartDuration = $("#cbbDuration").val();
    var chartEnd = '';
    var added_columns = $('#cbbAddedColumns').val();
    var arrStr = '';
    if(added_columns) {
        arrStr = added_columns.toString();
    }
    var show_by = $('#cbbShowBy').val();
    if ($('[id*="wbst-tab-"]').length > 0){
        // Neu graph_detail nam trong 'widget_by_station_type'
        show_by = $('#cbbShowBy-' + container.attr('data-station_type')).val();
        chartStart = $("#chartStart-" + container.attr('data-station_type')).val();
        chartDuration = $('#cbbDuration-' + container.attr('data-station_type')).val();
    }

    if (chartStart == undefined) {
        chartStart = $("#dt0_from_date").val();
        chartEnd = $("#dt0_to_date").val();
    }

    var target = '#slideStationCharts-' + stationId;
    app.showProgress(target);
    app.postAjax({
        showProgress: false,
        url: url,
        // data: {stationId: stationId, show_by: $('#hfShowby').val(), chart_start: chartStart, chart_end: chartEnd},

        data: {stationId: stationId, show_by: show_by, chart_start: chartStart, chart_end: chartEnd, duration: chartDuration, arrStr},
        callback: function (res) {
            app.hideProgress(target);
            var charts = res.charts;
            var carousel_indicators = "<ol class='carousel-indicators'>";
            var carousel_inner = "<div class=\"carousel-inner\">";
            var idx = 0;
            for (var key in charts) {
                if (!charts.hasOwnProperty(key)) {
                    continue;
                }
                if (idx == 0) {
//                    carousel_indicators += "<li data-target='#" + key + "-" + stationId + "' data-slide-to='" + idx + "' class='active'></li>";
                    carousel_inner += "<div id='" + key + "-" + stationId + "' class='item active'></div>";
                } else {
                    carousel_indicators += "<li data-target='#" + key + "-" + stationId + "' data-slide-to='" + idx + "'></li>";
                    carousel_inner += "<div id='" + key + "-" + stationId + "' class='item'></div>";
                }
                idx += 1;
            }
            carousel_indicators += "</ol>";
            carousel_inner += "</div>";
            container.find(target).html(carousel_indicators + carousel_inner);
            for (var key in charts) {
                if (!charts.hasOwnProperty(key)) {
                    continue;
                }
                var chartContainer =
                Highcharts.chart(key + '-' + stationId, {
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
    });
}

function createChartForStationForItem(indicatorId, container) {
    if (container == undefined){
        container = $('body');
    }
    if ($('[id*="wbst-tab-"]').length > 0){
        // Neu graph_detail nam trong 'widget_by_station_type'
        container = $('[id*="wbst-tab-"].active').find('.widget_graph_detail');
    }
    var stationId  = container.find('#hfStationId').val();
    var show_by = $('#cbbShowBy').val();
    var chartDuration = $("#cbbDuration").val();
    var chartStart = $("#chartStart").val();
    var chartEnd = $("#chartEnd").val();
    if ($('[id*="wbst-tab-"]').length > 0){
        // Neu graph_detail nam trong 'widget_by_station_type'
        show_by = $('#cbbShowBy-' + container.attr('data-station_type')).val();
        chartStart = $("#chartStart-" + container.attr('data-station_type')).val();
        chartDuration = $('#cbbDuration-' + container.attr('data-station_type')).val();
    }
    var url = $('#hfUrlGetChartForItem').val();
    
    if (chartStart == undefined) {
        chartStart = $("#dt0_from_date").val();
        chartEnd = $("#dt0_to_date").val();
    }
    var target = '#detailChart-' + stationId + '-' + indicatorId;
    app.showProgress(target);
    app.postAjax({
        url: url,
        showProgress: false,
        data: {stationId: stationId, show_by: show_by, indicatorId: indicatorId, chart_start: chartStart,chart_end: chartEnd, duration: chartDuration},
        callback: function (res) {
            app.hideProgress(target);
            if (!res.success){
                app.showError(res.message);
                return false;
            }
            var charts = res.charts;
            var $report = $('#report-' + stationId + '-' + indicatorId);
            var chartOption = {
                chart: {
                    type: 'line',
                    zoomType: 'x',
                    spacingBottom: 30,
                    height: 500,
                    events: {
                        selection: function (event) {
                            if (event.xAxis) {
                                $report.html('Last selection:<br/>min: ' + Highcharts.dateFormat('%Y-%m-%d', event.xAxis[0].min) +
                                    ', max: ' + Highcharts.dateFormat('%Y-%m-%d', event.xAxis[0].max));
                            } else {
                                $report.html('Selection reset');
                            }
                        },
                        load: function () {
                            if (show_by == $('#hfShowByMinute').val()) {
                                // Get start date and end date
                                var start = $($('.item.active .highcharts-range-input')[0]).text();
                                var end = $($('.item.active .highcharts-range-input')[1]).text();
                                if (start == '') {
                                    var today = new Date();
                                    var dd = today.getDate();
                                    var mm = today.getMonth() + 1; //January is 0!
                                    var yyyy = today.getFullYear();

                                    if (dd < 10) dd = '0' + dd;
                                    if (mm < 10) mm = '0' + mm;

                                    start = dd + '/' + mm + '/' + yyyy;
                                    end = start;
                                }
                                params = {
                                    station_id: container.find('#hfStationId').val(),
                                    indicator: indicatorId,
                                    from_time: start,
                                    to_time: end,
                                };
                                $('.graph_detail_adjust_data').attr('data-params', $.param(params));
                                $('.graph_detail_adjust_data').show();
                            } else {
                                $('.graph_detail_adjust_data').attr('data-params', '');
                                $('.graph_detail_adjust_data').hide();
                            }
                        }
                    },
                },
                rangeSelector: charts.rangeSelector,
                title: charts.title,
                subtitle: charts.subtitle,
                yAxis: {
                    title: charts.yAxis.title,
                    labels: {
                        formatter: function () {
                            return this.value;
                        }
                    }
                },
                credits: {
                    enabled: false
                },
                series: charts.series
            };

            Highcharts.stockChart('detailChart-' + stationId + '-' + indicatorId, chartOption);
        }
    });
}