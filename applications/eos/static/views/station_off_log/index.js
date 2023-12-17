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

    datepicker_start.max = new Date().toISOString().split("T")[0];
    datepicker_start.min = date_min;

    datepicker_end.max = new Date().toISOString().split("T")[0];
    datepicker_end.min = date_min;
    loadDataTableForPage();

    $('body').on('change', function () {
        datepicker_start =  $('#datepicker_start').val();
        datepicker_end =  $('#datepicker_end').val();
    });

    $('#btnExportExcel').on('click', function (e) {
        if ($('#datepicker_start').val() == '' && $('#datepicker_end').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
            column = table.column(1).data();
        }
        if ($('.dataTables_empty').text() != '') {
            e.preventDefault();
            app.showNotification({"content": app.translate('MSG_NO_DATA_EXPORT')});
            return false;
        }
        if ($('#datepicker_start').val() == '' && $('#datepicker_end').val() != '') {
            e.preventDefault();
            app.showError(app.translate('ERR_Day_Blank'));
            return false;
        }
        var datepicker_start =  $('#datepicker_start').val();
        var datepicker_end = $('#datepicker_end').val();

        var url = $(this).attr("data-url");
        var allParams = $(this).attr("data-params").split(",");
        var params = {
            'sSearch': $("#custom_datatable_0_filter input").val()
        };
        var total = allParams.length;
        for (var i = 0; i < total; i++){
            if (allParams[i].trim()!=""){
                var item = $("[name='" + allParams[i] + "']").first();
                if (item.length == 1 && item.val() !== null ) {
                    params[allParams[i].trim()] = item.val().toString();
                }
            }
        }
        
        if (url.indexOf("?") == -1){
            url += "?";
        }
        url += $.param(params);
        console.log('url', url)
        window.open(url);
    });

    $('#cbbStationType').change(function () {
        var url = $(this).data('url');
        var data = {};
        app.postAjax({
            url: url,
            data: {
                   station_type: $('#cbbStationType').val()
                  },
            callback: function (res) {
                if (res.success) {
                    $('#cbbArea').html(res.html);
                    $('#cbbArea').trigger("chosen:updated");
                    $('#cbbStationId').html(res.html2);
                    $('#cbbStationId').trigger("chosen:updated");
                    $('#cbbProvinceId').html(res.html1);
                    $('#cbbProvinceId').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('#cbbStationType').change(function () {
        var url = $(this).data('url');
        var careers = ""
        if ($("#cbbCareer").val() != null) {
            careers =$("#cbbCareer").val().join(",")
        }
        var data = {};
        app.postAjax({
            url: url,
            data: {
                   station_type: $('#cbbStationType').val(),
                   careers: careers,
                  },
            callback: function (res) {
                if (res.success) {
                    $('#cbbArea').html(res.html);
                    $('#cbbArea').trigger("chosen:updated");
                    $('#cbbStationId').html(res.html2);
                    $('#cbbStationId').trigger("chosen:updated");
                    $('#cbbProvinceId').html(res.html1);
                    $('#cbbProvinceId').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('#cbbProvinceId').change(function () {
        var url = $(this).data('url');
        var data = {};
        app.postAjax({
            url: url,
            data: {area_id: $('#cbbArea').val(),
                   station_type: $('#cbbStationType').val(),
                   province_id: $('#cbbProvinceId').val()
                  },
            callback: function (res) {
                if (res.success) {
                    $('#cbbStationId').html(res.html1);
                    $('#cbbStationId').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('#cbbArea').change(function () {
        var url = $(this).data('url');
        var x = $('#cbbArea').val()
        console.log('xxx', x)
        var data = {};
        app.postAjax({
            url: url,
            data: { area_id: $('#cbbArea').val(),
                    station_type: $('#cbbStationType').val(),
                    },
            callback: function (res) {
                if (res.success) {
                    $('#cbbStationId').html(res.html2);
                    $('#cbbStationId').trigger("chosen:updated");
                    $('#cbbProvinceId').html(res.html1);
                    $('#cbbProvinceId').trigger("chosen:updated");
                    $('#cbbStationType').html(res.html);
                    $('#cbbStationType').trigger("chosen:updated");
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

$('#cbbConnectionLoss').on('change', function (e) {
    e.preventDefault();
    var connection_loss = $(this).val();
    
   console.log("connection_losss", connection_loss)
});




function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%'},
        {'sWidth' : '17%'},
        {'sWidth' : '18%'},
        {'sWidth' : '10%'},
        {'sWidth' : '16%'},
        {'sWidth' : '12%'},
        {'sWidth' : '12%'},
        {'sWidth' : '12%'},
    ];

    var aoClass = ['', 'text-left', '', '', '', '', '', 'text-right'];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "type", "value": $('#cbbStationType').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "station_id", "value": $('#cbbStationId').val()
            });
            aoData.push({
                "name": "datepicker_start", "value": $('#datepicker_start').val()
            });
            aoData.push({
                "name": "datepicker_end", "value": $('#datepicker_end').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#cbbProvinceId').val()
            });
            aoData.push({
                "name": "area_id", "value": $('#cbbArea').val()
            });
            aoData.push({
                "name": "connection_loss", "value": $('#cbbConnectionLoss').val()
            });
        },
    });

    return true;
}