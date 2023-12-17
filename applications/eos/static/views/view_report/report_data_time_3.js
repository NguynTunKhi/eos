var isLoadDatatable = false;

$(document).ready(function () {
    $('#cbbAddedStations_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    $('#cbbAddedProvinces_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')

    $('#btnExportExcel').on('click', function (e) {
         if (!validateTime2())    {
            e.preventDefault();
            return false;
        }
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
            column = table.column(1).data();
            time_temp = column[0].split(' ').reverse()[0].split('/').reverse().join('-') + ' ' + column[0].split(' ').reverse()[1];
            time_export = new Date().getTime() - new Date(time_temp).getTime();
            month_export = new Date(time_export).getMonth()+1;
            if (month_export > 1) {
                e.preventDefault();
                app.showNotification({"content": app.translate('MSG_NO_DATA_EXPORT')});
                return false;
            }
        }
        if ($('.dataTables_empty').text() != '') {
            e.preventDefault();
            app.showNotification({"content": app.translate('MSG_NO_DATA_EXPORT')});
            return false;
        }
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() != '') {
            e.preventDefault();
            app.showError(app.translate('ERR_Day_Blank'));
            return false;
        }
        var url = $(this).attr("data-url");
            var allParams = $(this).attr("data-params").split(",");
            var params = {
                'sSearch': $("#custom_datatable_0_filter input").val()
            };
            var total = allParams.length;
            for (var i = 0; i < total; i++){
                if (allParams[i].trim()!=""){
                    var item = $("[name='" + allParams[i] + "']").first();
                    if (item.length == 1 && item.val() !== null) {
                        params[allParams[i].trim()] = item.val().toString();
                    }
                }
            }
            if (url.indexOf("?") == -1){
                url += "?";
            }
            url += $.param(params);
            window.open(url);
    });

    $('body').on('click', '#check_station', function (e) {
        if(e.target.checked){
            $('#cbbAddedStations option').prop('selected', true);
            $('#cbbAddedStations').trigger("change");
            $('#cbbAddedStations').trigger('chosen:updated');

        } else {
            $('#cbbAddedStations option:selected').removeAttr('selected');
            $('#cbbAddedStations').trigger("change");
            $('#cbbAddedStations').trigger('chosen:updated');
        }
    });


    $('body').on('click', '#check_province', function (e) {
        if(e.target.checked){
            $('#cbbAddedProvinces option').prop('selected', true);
            $('#cbbAddedProvinces').trigger("change");
            $('#cbbAddedProvinces').trigger('chosen:updated');

        } else {
            $('#cbbAddedProvinces option:selected').removeAttr('selected');
            $('#cbbAddedProvinces').trigger("change");
            $('#cbbAddedProvinces').trigger('chosen:updated');
        }
    });

    $('#cbbRatioCustom').change(function() {
        var ratio = $('#cbbRatioCustom').val();
        console.log(ratio)
         switch (ratio) {
            case ratio < '100' && ratio > '0':
                $('table .headerAll tr:nth-child(2) th:nth-child(1)').text('>='+ratio+'%');
                $('table .headerAll tr:nth-child(2) th:nth-child(2)').text('<='+ratio+'%');
                $('table .headerAll tr:nth-child(2) th:nth-child(3)').text('=0%');
                break;
//            case '12':
//                $('table tr:first th:nth-child(3)').text('Số lượng trạm bị gián đoạn truyền dữ liệu ≥12h');
//                break;
//            case '24':
//                $('table tr:first th:nth-child(3)').text('Số lượng trạm bị gián đoạn truyền dữ liệu ≥24h');
//                break;
//            case '48':
//                $('table tr:first th:nth-child(3)').text('Số lượng trạm bị gián đoạn truyền dữ liệu ≥48h');
//                break;
            default:
                $('table .headerAll tr:nth-child(2) th:nth-child(1)').text('>='+ratio+'%');
                $('table .headerAll tr:nth-child(2) th:nth-child(2)').text('<='+ratio+'%');
                $('table .headerAll tr:nth-child(2) th:nth-child(3)').text('=0%');
        }
    })

    $('body').on('click', '.btnCustomSearch', function (e) {
        time = new Date();
        date = new Date().toISOString().split("T")[0];

        if ($('#cbbReportType').val() == '') {
            e.preventDefault();
            app.showError(app.translate('Please select a report type!'));
            return false;
        }
        if (!validateTime())    {
            e.preventDefault();
            return false;
        }
        $('#btnExportExcel').removeClass('hide');
        oTable[0].fnFilter();
        if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
    });

    $('#cbbReportType').change(function () {
        if ($('#cbbReportType').val() == 'all') {
            $('.headerProvince').addClass('hide')
            $('.headerAll').removeClass('hide')
            $('#area').removeClass('hide');
            $('.chosen-container').css('width', '100%')
            $('#multiprovince').removeClass('hide');
            $('#multistation').addClass('hide');
            $('#province').addClass('hide');
            $('table tr:first th:nth-child(2)').text('Tỉnh/TP');
            $('#cbbStationType').attr("data-url","/eos/view_report/call/json/get_provinces_and_area")
            $('#btnExportExcel').attr("data-params", "station_type,from_date,to_date,province_id,data_type,area_id,report_type,added_provinces,careers,custom_ratio")
            loadDataTableForPage()
        }
        if ($('#cbbReportType').val() == 'province') {
            $('.headerAll').addClass('hide')
            $('.headerProvince').removeClass('hide')
            $('#area').addClass('hide');
            $('#province').removeClass('hide');
            $('#multistation').removeClass('hide');
            $('#multiprovince').addClass('hide');
            $('table tr:first th:nth-child(2)').text('Tên trạm');
            $('#cbbStationType').attr("data-url","/eos/view_report/call/json/get_stations_and_province")
            $('#btnExportExcel').attr("data-params", "station_type,from_date,to_date,province_id,data_type,area_id,report_type,added_stations,careers,custom_ratio")
            loadDataTableForPage()
        }

    })

    $('#cbbStationType').change(function () {
        var url = $(this).data('url');
        var carrers = "";
        if ($("#cbbCareer").val() !== null) {
            carrers = $("#cbbCareer").val().join(",")
        }

        app.postAjax({
            url: url,
            data: {
                type: $('#cbbStationType').val(),
                province_id: $('#cbbProvinceId').val(),
                carrers: carrers,
            },
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedStations').html(res.html_2);
                    $('#cbbAddedStations').trigger("change");
                    $('#cbbAddedStations').trigger("chosen:updated");

                    $('#cbbProvinceId').html(res.html);
                    $('#cbbProvinceId').trigger("chosen:updated");

                    $('#cbbArea').html(res.html1);
                    $('#cbbArea').trigger("chosen:updated");
                    $('#cbbAddedProvinces').html(res.html);
                    $('#cbbAddedProvinces').trigger("change");
                    $('#cbbAddedProvinces').trigger("chosen:updated");
                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#cbbStationId').val() == '') $('#btnExportExcel').addClass('hide');
    });

    $('#cbbCareer').change(function () {
        var url = $(this).data('url');
         var carrers = "";
        if ($("#cbbCareer").val() !== null) {
            carrers = $("#cbbCareer").val().join(",")
        }

        app.postAjax({
            url: url,
            data: {
                type: $('#cbbStationType').val(),
                province_id: $('#cbbProvinceId').val(),
                carrers: carrers,
            },
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedStations').html(res.html_2);
                    $('#cbbAddedStations').trigger("change");
                    $('#cbbAddedStations').trigger("chosen:updated");

                    $('#cbbProvinceId').html(res.html);
                    $('#cbbProvinceId').trigger("chosen:updated");

                    $('#cbbArea').html(res.html1);
                    $('#cbbArea').trigger("chosen:updated");
                    $('#cbbAddedProvinces').html(res.html);
                    $('#cbbAddedProvinces').trigger("change");
                    $('#cbbAddedProvinces').trigger("chosen:updated");
                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#cbbStationId').val() == '') $('#btnExportExcel').addClass('hide');
    });

    $('#cbbArea').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {type: $('#cbbStationType').val(),
                    area: $('#cbbArea').val()},
            callback: function (res) {
                if (res.success) {
                    $("#check_province").attr("checked", true)
                    $('#cbbAddedProvinces').html(res.html);
                    $('#cbbAddedProvinces').trigger("change");
                    $('#cbbAddedProvinces').trigger("chosen:updated");
                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('#cbbProvinceId').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {type: $('#cbbStationType').val(),
                    province_id: $('#cbbProvinceId').val()},
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedStations').html(res.html_2);
                    $('#cbbAddedStations').trigger("change");
                    $('#cbbAddedStations').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#cbbStationId').val() == '') $('#btnExportExcel').addClass('hide');
    });

    $('#dt0_to_date').val(new Date().toISOString().split("T")[0]);
    time = new Date($('#dt0_to_date').val());
    time.setDate(time.getDate() - 30);
    date_min = time.toISOString().split("T")[0];
    $('#dt0_from_date').val(date_min);
    if ($('#cbbProvinceId').val()) {
        $('#cbbProvinceId').trigger('change');
    }
    if ($('#cbbStationId').val()) {
        isLoadDatatable = true;
        $('#cbbStationId').trigger('change');
    } else {
        loadDataTableForPage();
    }
});
function validateTime2() {
    var dt0_from_date = $('#dt0_from_date');
    var dt0_to_date = $('#dt0_to_date');
    var fromDate = new Date(dt0_from_date.val());
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime( maxDate.getTime() + myTimeZone * 60 * 60 * 1000 );
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val()=='')    {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#dt0_to_date').val(tempDate);
        minDate = new Date();
    }
    minDate.setMonth(minDate.getMonth()-1);
    // if (fromDate < minDate) {
    //     app.showError(app.translate('ERR_Excel_Export_1_Month'));
    //     return false;
    // }
    return true;
}
function validateTime() {
    var dt0_from_date = $('#dt0_from_date');
    var dt0_to_date = $('#dt0_to_date');
    if (dt0_from_date.val()=='')
    {
        app.showError(app.translate('ERR_Day_Input_Blank'));
        return false;
    }
    var fromDate = new Date(dt0_from_date.val());
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime( maxDate.getTime() + myTimeZone * 60 * 60 * 1000 );
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val()=='')    {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#dt0_to_date').val(tempDate);
        minDate = new Date();
    }
    minDate.setDate(minDate.getDate()-3*365);
    if (toDate>maxDate)  {
        app.showError(app.translate('ERR_Day_Input_To_Date_Max_Exceed'));
        return false;
    }
    if (fromDate > toDate) {
        app.showError(app.translate('ERR_Day_Search'));
        return false;
        // $('#dt0_to_date').val('');
    }
    // if (fromDate < minDate) {
    //     app.showError(app.translate('ERR_Day_Input_From_Date_1_YEAR'));
    //     return false;
    // }
    return true;
}
function loadDataTableForPage() {

    if ($('#cbbReportType').val() == 'all') {
        var sAjaxSource = $("#custom_datatable_0").attr("data-url");
        var aoColumns = [
            {'sWidth': '3%'},
            {'sWidth': '20%'},
            {'sWidth': '20%'},
            {'sWidth': '20%'},
            {'sWidth': '20%'},
            {'sWidth': '20%'},
        ];
    
        var aoClass = ['', 'text-left', ''];
        loadDataTable({
            sAjaxSource: sAjaxSource,
            aoColumns: aoColumns,
            aoClass: aoClass,
        });
        return true;
    } else {
        var sAjaxSource = $("#custom_datatable_0").attr("data-url");
        var aoColumns = [
            {'sWidth': '3%'},
            {'sWidth': '20%'},
            {'sWidth': '20%'},
            {'sWidth': '20%'},
        ];
    
        var aoClass = ['', 'text-left', ''];
        loadDataTable({
            sAjaxSource: sAjaxSource,
            aoColumns: aoColumns,
            aoClass: aoClass,
        });
        return true;
    }
   
}
