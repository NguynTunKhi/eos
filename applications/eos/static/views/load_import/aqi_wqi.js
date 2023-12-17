
var aqiInterval = setInterval(function () {
    if (typeof jQuery == 'function'){
        $(document).ready(function() {
            loadDataTableForPage_aqi_wqi();
            
            $('.scroll_aw').slimscroll({
                height: '341px'
            });
            $('.scroll_aw_detail').slimscroll({
                height: '375px'
            });
            
            // Select station on left list --> display detail info on the right panel
            $('body').on('click', '#custom_datatable_aw tbody tr' , function(e){
                if ($(this).hasClass('selected')){
                    // Click vao row dang dc select --> ko lam gi ca
                } else {
                    $(this).closest('tbody').find('tr').removeClass('selected');
                    $(this).addClass('selected');
                    var station_id = $(this).data('id');

                    // Set Station name in header of block detail on the right
                    var name = $(this).find('td.text-left').html();
                    $('#aqi_station_name').html(name);
                    
                    // Call action to redraw right panel
                    var url = $('#hfUrlLoadAQI').val();
                    
                    url += "?" + $.param({station_id: station_id});
                    // $("#aqi_detail").load(url);
                    $("#aqi_detail").load(url, function(){
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
                    });
                }
            });
            
        });
        clearInterval(aqiInterval);
    }
}, 100);


function loadDataTableForPage_aqi_wqi() {
    var aoColumns = [
        {'sWidth' : '55%'},
        {'sWidth' : '15%'},
        {'sWidth' : '15%'},
        {'sWidth' : '15%'},
    ];

    var aoClass = ['text-left', 'text-left', '', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable: 'aw',
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "area_id", "value": $('#global_area_id').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#global_province_id').val()
            });
        },
    });
    
    //chinh CSS cua table list station
    var wrap = $('#custom_datatable_aw').closest('.middle');
    wrap.removeClass('row');
    
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