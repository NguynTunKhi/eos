$(document).ready(function() {
    $('#dt0_to_date').val(new Date().toISOString().split("T")[0]);
    time = new Date($('#dt0_to_date').val());
    time.setDate(time.getDate() - 7);
    date_min = time.toISOString().split("T")[0];
    $('#dt0_from_date').val(date_min);

    loadDataTableForPage();
    $('#btn_search').click(function () {
        if (!validateTime())    {
            e.preventDefault();
            return false;
        }
        oTable[0].fnFilter('');
    });
    /*$('body').on('click', '.btnSearch', function (e) {
        if (!validateTime()) {
             e.preventDefault();
            return false;
        }
        return true;
        // oTable[0].fnFilter('');
    });*/
    $('body').on('click', '#check', function (e) {
        if(e.target.checked){
            $('#cbbAddedColumns option').prop('selected', true);
            $('#cbbAddedColumns').trigger("change");
            $('#cbbAddedColumns').trigger('chosen:updated');

        } else {
            $('#cbbAddedColumns option:selected').removeAttr('selected');
            $('#cbbAddedColumns').trigger("change");
            $('#cbbAddedColumns').trigger('chosen:updated');
        }
    });
});
$('#cbbStationType, #cbbProvinceId').change(function () {
        var url = $(this).data('url');
        var data = {};
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

    $('#cbbStationId').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {station_id: $('#cbbStationId').val()},
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedColumns').html(res.html);
                    $('#cbbAddedColumns').trigger("change");
                    $('#cbbAddedColumns').trigger("chosen:updated");
                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#cbbStationId').val() == '') $('.btnExport').addClass('hide');

        // if ($('li.graph.active').length > 0){
        // loadGraphicForStation();
        // }
        // if ($(this).val() != '') {
        // $('.btnExport').removeClass('hide');
        // } else {
        // $('.btnExport').addClass('hide');
        // }
    });

$('#btnExportExcel').on('click', function (e) {
        var url = $(location).attr("href").split("/").pop();
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
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
    minDate.setDate(minDate.getDate()- 3*365);
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
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '2%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'}, 
    ];

    var aoClass = ['', 'text-left', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        // fnCustomServerData: function (sSource, aoData, fnCallback) {
            // aoData.push({
                // "name": "from_date", "value": $('#from_date').val()
            // });
            // aoData.push({
                // "name": "to_date", "value": $('#to_date').val()
            // }); 
            // aoData.push({
                // "name": "sometext", "value": $('#sometext').val()
            // });
        // },
    });
    
    return true;
}

// function reloadDatatable_alarm_logs() {
    // oTable[0].fnDraw();
// }