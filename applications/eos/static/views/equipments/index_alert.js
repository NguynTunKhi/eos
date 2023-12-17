$(document).ready(function () {
    loadDataTableForPage();

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
                    if (item.length == 1 && item.val() !== null ) {
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

    $('#btn_search').click(function () {
        if (!validateTime())    {
            e.preventDefault();
            return false;
        }
        $('#btnExportExcel').removeClass('hide');
        oTable[0].fnFilter('');
    });

    $('#type, #province_id, #area_id').change(function () {
        var url = $(this).data('url');
        var data = {};
        app.postAjax({
            url: url,
            data: {filter_value: $('#type').val().trim() + ';' + $('#province_id').val().trim() + ';' + $('#area_id').val().trim()},

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


    $('#dt0_to_date').val(new Date().toISOString().split("T")[0]);
        time = new Date($('#dt0_to_date').val());
        time.setDate(time.getDate() - 14);
        date_min = time.toISOString().split("T")[0];
        $('#dt0_from_date').val(date_min);


});

function validateTime() {
    var dt0_from_date = $('#dt0_from_date');
    var dt0_to_date = $('#dt0_to_date');
    if (dt0_from_date.val() == '') {
        app.showError(app.translate('ERR_Day_Input_Blank'));
        return false;
    }
    var fromDate = new Date(dt0_from_date.val());
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime( maxDate.getTime() + myTimeZone * 60 * 60 * 1000 );
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val() == '') {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#dt0_to_date').val(tempDate);
        minDate = new Date();
    }
    minDate.setDate(minDate.getDate() - 3*365);
    if (toDate > maxDate) {
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

    return true;
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var province_id = $("#province_id").val();
    var area_id = $("#area_id").val();
    var station_type = $("#type").val();
    var aoColumns = [
        {'sWidth': '2%'},
        {'sWidth': '15%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
        {'sWidth': '10%'},
    ];

    var aoClass = ['', 'text-left', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "station_type", "value": $('#type').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#province_id').val()
            });
            aoData.push({
                "name": "area_id", "value": $('#area_id').val()
            });
            aoData.push({
                "name": "station_id", "value": $('#cbbStationId').val()
            });
            aoData.push({
                "name": "from_date", "value": $('#dt0_from_date').val()
            });aoData.push({
                "name": "status", "value": $('#dt0_status').val()
            });
            aoData.push({
                "name": "to_date", "value": $('#dt0_to_date').val()
            });
        },
    });

    return true;
}
