$(document).ready(function() {
    date = new Date().toISOString().split("T")[0];
    date_min = new Date().toISOString().split("T")[0];
    year = date.split('-');
    year_min = date_min.split('-');
    min_year =  parseInt(year_min[0])  -1;
    start_day = parseInt(year[2])  -1;
    date_min = date_min.replace(year_min[0],min_year.toString());
    date_min = date_min.replace(year_min[1],'01');
    date_min = date_min.replace(year_min[2],'01');
    date_max_start_day =  date.replace(year[2],start_day.toString());

    from_date.max = new Date().toISOString().split("T")[0];
    from_date.min = date_min;

    to_date.max = new Date().toISOString().split("T")[0];
    to_date.min = date_min;

    loadDataTableForPage();
    

    $('body').on('change', function () {
        datepicker_start =  $('#datepicker_start').val();
        datepicker_end =  $('#datepicker_end').val();

    });
    $('#cbbStationType, #cbbProvinceId').change(function () {
        var url = $(this).data('url');
        var data = {};
        var a = $('#cbbStationType').val().trim();
        var b = $('#cbbProvinceId').val().trim();
        app.postAjax({
            url: url,
            data: {filter_value: $('#cbbStationType').val().trim() + ';' + $('#cbbProvinceId').val().trim()},
            callback: function (res) {
                if (res.success) {
                    $('#cbbStationId').html(res.html);
                    $('#cbbStationId').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%'},
        {'sWidth' : '12%'},
        {'sWidth' : '9%'},
        {'sWidth' : '6%'},
        {'sWidth' : '31%'},
        {'sWidth' : '25%'},
        {'sWidth' : '8%'},
        {'sWidth' : '3%'},
        {'sWidth' : '3%'},
    ];

    var aoClass = ['', 'text-left', '', '', 'text-left', 'text-left', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "from_date", "value": $('#from_date').val()
            });
            aoData.push({
                "name": "to_date", "value": $('#to_date').val()
            });
            aoData.push({
                "name": "alarm_level", "value": $('#alarm_level').val()
            });
            aoData.push({
                "name": "status", "value": $('#status').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "station_type", "value": $('#cbbStationType').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#cbbProvinceId').val()
            });
            aoData.push({
                "name": "station_id", "value": $('#cbbStationId').val()
            });
        },
    });
    
    return true;
}

function reloadDatatable_alarm_logs() {
    oTable[0].fnDraw();
}