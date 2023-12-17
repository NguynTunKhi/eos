var widgetAQI_Interval = setInterval(function () {
    if (typeof jQuery == 'function' && typeof Highcharts == 'object'){
        clearInterval(widgetAQI_Interval);
        $(document).ready(function(){
            $('body').off('change', '#widget_aqi_station');
            $('body').on('change', '#widget_aqi_station', function (e) {
                widgetAQICreateChart();
            });

            $('#widget_aqi_station').trigger('change');
        });
    }
}, 30);

function widgetAQICreateChart() {
    var stationId  = $('#widget_aqi_station').val();
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
                    type: 'bar'
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
