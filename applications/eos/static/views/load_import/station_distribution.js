var station_distribution_interval = setInterval(function () {
    if (typeof jQuery == 'function'){
        $(document).ready(function(){
            getDataForStationDistributionChart();

            $('body').off('click', '.btnStationDistribution');
            $('body').on('click', '.btnStationDistribution', function (e) {
                $('.btnStationDistribution').removeClass('active');
                $(this).addClass('active');
                
                getDataForStationDistributionChart();
            });
        });
        clearInterval(station_distribution_interval);
    }
}, 300);

function getDataForStationDistributionChart() { 
    var byProvince = false;
    var url = '';
    
    // Neu Global province/area co gtri thi load chart theo cac tram, voi chi so, loai : Stack chart
    if ($('#global_province_id').val() != '' || $('#global_area_id').val() != '') {
        var params = {
            area_id: $('#global_area_id').val(),
            province_id: $('#global_province_id').val(),
        };
        
        url = $('.btnStationDistribution.active').data('url2') + '?' + $.param(params);
        byProvince = true;
    } else {
        url = $('.btnStationDistribution.active').data('url');
    }  
    app.showProgress('#distributeChart');
    app.postAjax({
        url: url,
        showProgress: false,
        data: {},
        callback: function (res) {
            app.hideProgress('#distributeChart');
            if (byProvince == false) {
                createStationDistributionChart(res.data);
            } else {
                createProvinceStationDataChart(res.data);
            }
        }
    });
}

function createProvinceStationDataChart(data) { 
    Highcharts.chart('distributeChart', {
        chart: {
            type: 'column'
            // backgroundColor: '#f3f3f4'
        },
        title: {
            text: data.title
        },
        subtitle: {
            text: data.subtitle
        },
        credits: {
            enabled: false
        },
        xAxis: [{
            categories: data.categories,
        }],
        yAxis: [{
            title: {
                text: 'Type data',
//                text: 'Loại dữ liệu thu thập',
            },
        }],
        tooltip: {
            // shared: true,
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal} ({point.percentage.2f}%)',
            formatter: function() {
                return this.series.name + ': <b>' + this.y + '</b> ('+ this.percentage.toFixed(2) + '%)';
            }
        },
        legend: {
            align: 'left',
            x: 60,
            verticalAlign: 'top',
            y: 35,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || 'rgba(255,255,255,0.25)',
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        series: data.series
    });
}

function createStationDistributionChart(data) {

    // Build DISTRIBUTE charts
    Highcharts.chart('distributeChart', {
        chart: {
            zoomType: 'x',
            type: 'column'
            // backgroundColor: '#f3f3f4'
        },
        title: {
            text: data.title
        }, 
        subtitle: {
            text: data.subtitle
        },
        credits: {
            enabled: false
        },
        xAxis: [{
            categories: data.categories,
            // crosshair: true
        }],
        yAxis: [{
            title: {
                text: app.translate('Number of Stations'),
            },
        }],
        tooltip: {
            shared: true
        },
        legend: {
            align: 'left',
            x: 60,
            verticalAlign: 'top',
            y: 35,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || 'rgba(255,255,255,0.25)',
        },
        // legend: {
        //     align: 'left',
        //     x: 60,
        //     verticalAlign: 'top',
        //     y: 35,
        //     floating: true,
        //     symbolPadding: 0,
        //     symbolWidth: 0.1,
        //     symbolHeight: 0.1,
        //     symbolRadius: 0,
        //     useHTML: true,
        //     backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || 'rgba(255,255,255,0.25)',
        //     labelFormatter: function() {
        //         if(this.index==0){
        //             return '<div  style="width:100px"><p style="margin-left:10px"><img src = \"../static/views/load_import/af1.png\" width = "auto" style="margin-right:10px;background-color:' + this.color + ';">' + this.name+ '</p></div>';
        //         }
        //         if(this.index==1){
        //             return '<div style="width:100px"><p style="margin-left:10px"><img src = \"../static/views/load_import/af2.png\"  width = "auto"  style="margin-right:10px;background-color:' + this.color + ';">' + this.name + '</p></div>';
        //         }
        //         if(this.index==2){
        //             return '<div style="width:200px"><p style="margin-left:10px"><img src = \"../static/views/load_import/af3.png\"  width = "auto"  style="margin-right:10px;background-color:' + this.color + ';">' + this.name + '</p></div>';
        //         }
        //     },
        // },
        // plotOptions: {
            // series: {
                // fillOpacity: 0.1
            // }
        // },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        series: data.series
    });
}