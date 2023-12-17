var isLoadDatatable = false;

$(document).ready(function () {
    $('#cbbAddedColumns_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    setViewAvgByMinute();

    if ($('li.search_result').hasClass('active')) {
        $('#btnExportExcel_min_max').hide();
        $('#btnExportExcel_chart').hide();
    }

    $('body').on('click', '#check', function (e) {
        if (e.target.checked) {
            $('#cbbAddedColumns option').prop('selected', true);
            $('#cbbAddedColumns').trigger("change");
            $('#cbbAddedColumns').trigger('chosen:updated');

        } else {
            $('#cbbAddedColumns option:selected').removeAttr('selected');
            $('#cbbAddedColumns').trigger("change");
            $('#cbbAddedColumns').trigger('chosen:updated');
        }
    });

    $('body').on('click', 'li.min_max', function (e) {
        if (!oTable[1]) {
            loadDataTableForPage_maxmin();
        }
        $('#btnExportExcel').hide();
        $('#btnExportExcel_min_max').show();
        $('#btnExportExcel_chart').hide();

    });

    $('body').on('click', 'li.search_result', function (e) {
        if (!oTable[1]) {
            loadDataTableForPage_maxmin();
        }
        $('#btnExportExcel').show();
        $('#btnExportExcel_min_max').hide();
        $('#btnExportExcel_chart').hide();
    });

    $("#viewType").change(function () {
        updateViewFilter();
    });

    $('#btnExportExcel').on('click', function (e) {
        var url = $(location).attr("href").split("/").pop();
        if (url == "index?view_type=1") {
            if (!validateTime2()) {
                e.preventDefault();
                return false;
            }
        } else {
            if (!validateTime3()) {
                e.preventDefault();
                return false;
            }
        }

        /*$('#custom_datatable_0').on('search.dt', function () {
                 var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
                var column = table.column(1).data();
            alert(column[0]);
        })
            .dataTable();*/
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
            column = table.column(1).data();
            time_temp = column[0].split(' ').reverse()[0].split('/').reverse().join('-') + ' ' + column[0].split(' ').reverse()[1];
            time_export = new Date().getTime() - new Date(time_temp).getTime();
            month_export = new Date(time_export).getMonth() + 1;
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
        for (var i = 0; i < total; i++) {
            if (allParams[i].trim() != "") {
                var item = $("[name='" + allParams[i] + "']").first();
                if (item.length == 1 && item.val() !== null ) {
                    params[allParams[i].trim()] = item.val().toString();
                }
            }
        }
        if (url.indexOf("?") == -1) {
            url += "?";
        }
        url += $.param(params);
        window.open(url);
    });


    $('#btnExportExcel_min_max').on('click', function (e) {
        var url = $(location).attr("href").split("/").pop();
        if (url == "index?view_type=1") {
            if (!validateTime2()) {
                e.preventDefault();
                return false;
            }
        } else {
            if (!validateTime3()) {
                e.preventDefault();
                return false;
            }
        }

        /*$('#custom_datatable_0').on('search.dt', function () {
                 var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
                var column = table.column(1).data();
            alert(column[0]);
        })
            .dataTable();*/
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
            column = table.column(1).data();
            time_temp = column[0].split(' ').reverse()[0].split('/').reverse().join('-') + ' ' + column[0].split(' ').reverse()[1];
            time_export = new Date().getTime() - new Date(time_temp).getTime();
            month_export = new Date(time_export).getMonth() + 1;
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
        for (var i = 0; i < total; i++) {
            if (allParams[i].trim() != "") {
                var item = $("[name='" + allParams[i] + "']").first();
                if (item.length == 1 && item.val() !== null ) {
                    params[allParams[i].trim()] = item.val().toString();
                }
            }
        }
        if (url.indexOf("?") == -1) {
            url += "?";
        }
        url += $.param(params);
        window.open(url);
    });

    $('#btnExportExcel_chart').on('click', function (e) {
        var url = $(location).attr("href").split("/").pop();
        if (url == "index?view_type=1") {
            if (!validateTime2()) {
                e.preventDefault();
                return false;
            }
        } else {
            if (!validateTime3()) {
                e.preventDefault();
                return false;
            }
        }

        /*$('#custom_datatable_0').on('search.dt', function () {
                 var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
                var column = table.column(1).data();
            alert(column[0]);
        })
            .dataTable();*/
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
            column = table.column(1).data();
            time_temp = column[0].split(' ').reverse()[0].split('/').reverse().join('-') + ' ' + column[0].split(' ').reverse()[1];
            time_export = new Date().getTime() - new Date(time_temp).getTime();
            month_export = new Date(time_export).getMonth() + 1;
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
        for (var i = 0; i < total; i++) {
            if (allParams[i].trim() != "") {
                var item = $("[name='" + allParams[i] + "']").first();
                if (item.length == 1 && item.val() !== null ) {
                    params[allParams[i].trim()] = item.val().toString();
                }
            }
        }
        if (url.indexOf("?") == -1) {
            url += "?";
        }
        url += $.param(params);
        window.open(url);
    });


    $('#btnExportCSV').on('click', function (e) {
        /*$('#custom_datatable_0').on('search.dt', function () {
                 var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
                var column = table.column(1).data();
            alert(column[0]);

        })
            .dataTable();*/
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
            column = table.column(1).data();
            time_temp = column[0].split(' ').reverse()[0].split('/').reverse().join('-') + ' ' + column[0].split(' ').reverse()[1];
            time_export = new Date().getTime() - new Date(time_temp).getTime();
            month_export = new Date(time_export).getMonth() + 1;
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
    });

    $('body').on('click', '.btnCustomSearch', function (e) {
        time = new Date();
        date = new Date().toISOString().split("T")[0];

        if ($('#cbbDuration').length > 0) {
            time.setDate(time.getDate() - $('#cbbDuration option:selected').val());
            var date_change = new Date(time).toISOString().split("T")[0];
        }

        if (!$('#cbbStationId').val()) {
            e.preventDefault();
            app.showError(app.translate('Please select a station first!'));
            return false;
        }
        if (!validateTime()) {
            e.preventDefault();
            return false;
        }
        $('.btnExport').removeClass('hide');
        if ($('li.min_max.active').length > 0) {
            oTable[0].fnFilter();
            oTable[1].fnFilter();
        } else if ($('li.graph.active').length > 0) {
            loadGraphicForStation();
        } else if ($('li.search_result.active').length > 0) {
            oTable[0].fnFilter();
            if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
        }
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
                console.log(res)
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
    $('#dt0_to_date').val(new Date().toISOString().split("T")[0]);
    time = new Date($('#dt0_to_date').val());
    time.setDate(time.getDate() - 30);
    date_min = time.toISOString().split("T")[0];
    $('#dt0_from_date').val(date_min);

    // $('#dt0_to_date').on('click', function () {
    //     if ($('#dt0_from_date').val() != '' && $('#dt0_to_date').val() != '') {
    //         var time = new Date($('#dt0_to_date').val());
    //         time.setDate(time.getDate() - 365);
    //         var min = time.toISOString().split("T")[0];
    //         $('#dt0_to_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: Date.now(),
    //         });
    //     } else {
    //         var time = new Date();
    //         time.setDate(time.getDate() - 365);
    //         var min = time.toISOString().split("T")[0];
    //         $('#dt0_to_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: Date.now(),
    //         });
    //     }
    //
    // });
    // $('#dt0_to_date').on('change', function () {
    //     if ($('#dt0_from_date').val() == '' || $('#dt0_to_date').val() == '') {
    //         var time = new Date();
    //         time.setDate(time.getDate() - 365);
    //         var min = time.toISOString().split("T")[0];
    //         $('#dt0_to_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: Date.now(),
    //         });
    //     }
    //
    //     var dt = new Date().toISOString().split('T')[0];
    //     if ($('#dt0_to_date').val() != '') {
    //         if ($('#dt0_to_date').val() > dt) {
    //             $('#dt0_to_date').val('');
    //             app.showError(app.translate('ERR_Day_Input_To_Date'));
    //         }
    //     }
    //     if ($('#dt0_from_date').val() != '' && $('#dt0_to_date').val() != '') {
    //         $('#dt0_to_date').datetimepicker({
    //             timepicker: false,
    //             formatDate: 'Y/m/d',
    //             minDate: $('#dt0_from_date').val(),
    //             maxDate: '-1970/01/01'
    //         });
    //
    //         if ($('#dt0_from_date').val() > $('#dt0_to_date').val()) {
    //             app.showError(app.translate('ERR_Day_Search'));
    //             $('#dt0_to_date').val('');
    //         }
    //     } /*else {
    //         app.showError(app.translate('ERR_Day_Blank'));
    //     }*/
    // });
    //
    // $('#dt0_from_date').on('click', function () {
    //     if ($('#dt0_from_date').val() == '' || $('#dt0_to_date').val() == '') {
    //         var time = new Date();
    //         time.setDate(time.getDate() - 365);
    //         var min = time.toISOString().split("T")[0];
    //         $('#dt0_from_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: Date.now()
    //         });
    //     } else if ($('#dt0_to_date').val() != '') {
    //         var time = new Date($('#dt0_to_date').val());
    //         time.setDate(time.getDate() - 365);
    //         var min = time.toISOString().split("T")[0];
    //         $('#dt0_from_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: $('#dt0_to_date').val()
    //         });
    //     }
    // });
    // $('#dt0_from_date').on('change', function () {
    //     if ($('#dt0_from_date').val() == '' || $('#dt0_to_date').val() == '') {
    //        var time = new Date();
    //         time.setDate(time.getDate() - 365);
    //         var min = time.toISOString().split("T")[0];
    //         $('#dt0_from_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: Date.now()
    //         });
    //     } else if ($('#dt0_to_date').val() != '') {
    //         var time = new Date($('#dt0_to_date').val());
    //         time.setDate(time.getDate() - 365);
    //         var min = time.toISOString().split("T")[0];
    //         $('#dt0_from_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: $('#dt0_to_date').val()
    //         });
    //     }
    //     if ($('#dt0_from_date').val() != '') {
    //         if ($('#dt0_from_date').val() < min) {
    //             $('#dt0_from_date').val('');
    //             app.showError(app.translate('ERR_Day_Input_From_Date'));
    //         }
    //     }
    //     if ($('#dt0_to_date').val() != '' && $('#dt0_from_date').val() != '') {
    //         $('#dt0_from_date').datetimepicker({
    //             timepicker: false,
    //             minDate: min,
    //             maxDate: $('#dt0_to_date').val()
    //         });
    //         if ($('#dt0_from_date').val() > $('#dt0_to_date').val()) {
    //             app.showError(app.translate('ERR_Day_Search'));
    //             $('#dt0_from_date').val('');
    //         }
    //     } /*else {
    //         app.showError(app.translate('ERR_Day_Blank'));
    //     }*/
    // });
    $('body').off('click', 'ul.nav.nav-tabs li.graph');
    $('body').on('click', 'ul.nav.nav-tabs li.graph', function (e) {
        loadGraphicForStation();
        $('#btnExportExcel').hide();
        $('#btnExportExcel_min_max').hide();
        $('#btnExportExcel_chart').show();
    });

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
    maxDate.setTime(maxDate.getTime() + myTimeZone * 60 * 60 * 1000);
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val() == '') {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#dt0_to_date').val(tempDate);
        minDate = new Date();
    }

    minDate.setDate(minDate.getDate() - 31);
//    if (fromDate < minDate) {
//        app.showError(app.translate('ERR_Excel_Export_1_Month'));
//        return false;
//    }
    return true;
}

function validateTime3() {
    var dt0_from_date = $('#dt0_from_date');
    var dt0_to_date = $('#dt0_to_date');
    var fromDate = new Date(dt0_from_date.val());
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime(maxDate.getTime() + myTimeZone * 60 * 60 * 1000);
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val() == '') {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#dt0_to_date').val(tempDate);
        minDate = new Date();
    }

    minDate.setDate(minDate.getDate() - 3 * 365);
    if (fromDate < minDate) {
        app.showError(app.translate('ERR_Day_Input_To_Date_Max_Exceed'));
        return false;
    }

    return true;
}

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
    maxDate.setTime(maxDate.getTime() + myTimeZone * 60 * 60 * 1000);
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val() == '') {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#dt0_to_date').val(tempDate);
        minDate = new Date();
    }
    //minDate.setDate(minDate.getDate() - 365);
    if (toDate > maxDate) {
        app.showError(app.translate('ERR_Day_Input_To_Date_Max_Exceed'));
        return false;
    }
    if (fromDate > toDate) {
        app.showError(app.translate('ERR_Day_Search'));
        return false;
        // $('#dt0_to_date').val('');
    }
//        if (fromDate < minDate) {
//            app.showError(app.translate('ERR_Day_Input_From_Date_1_YEAR'));
//            return false;
//        }
    return true;
}

function loadGraphicForStation() {
    var stationId = $('#cbbStationId').val();
    if (stationId) {
        var show_by = $('#viewType').val();
        var url = $('#hfUrlLoadGraph').val();
        var added_columns = $('#cbbAddedColumns').val();
        var arrStr = added_columns.toString();

        // 2 bien Start / From duoc lay o 'load_import/graph_detail.js

        url += "?" + $.param({station_id: stationId, show_by: show_by, arrStr});
        $("#graph_detail").load(url);

        // Display adjust data button
        $('#adjust_data').removeClass('hide');
    } else {
        $("#graph_detail").html(app.translate('No data found!'));
    }
}


function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth': '3%'},
        {'sWidth': '20%'},
    ];

    var aoClass = ['', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });

    return true;
}

function loadDataTableForPage_maxmin() {
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [
        {'sWidth': '3%'},
        {'sWidth': '17%'},
        {'sWidth': '15%'},
        {'sWidth': '15%'},
        {'sWidth': '15%'},
        {'sWidth': '15%'},
        {'sWidth': '15%'},
    ];

    var aoClass = ['', '', '', '', '', '', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        iTable: 1,
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            var fields = $('[data-forDT="0"]');
            var total = fields.length;
            for (var i = 0; i < total; i++) {
                var fieldName = $(fields[i]).attr('name');
                if (fieldName != undefined) {
                    if ($(fields[i]).attr('type') == 'checkbox') {
                        if ($(fields[i]).prop('checked')) {
                            $(fields[i]).attr('value', 1);
                        } else {
                            $(fields[i]).attr('value', '');
                        }
                    }
                    var fieldId = $(fields[i]).attr('id');
                    aoData.push({
                        "name": fieldName, "value": $('#' + fieldId).val()
                    });
                }
            }
            console.log('data min', fnCallback)
        }
    });

    return true;
}

function updateViewFilter() {
    var viewType = $("#viewType").val();
    switch (viewType) {
        case "1":
            setViewAvgByMinute();
            break;
        case "2":
            setViewAvgByHour();
            break;
        case "3":
            setViewAvgByDay();
            break;
        case "4":
            setViewAvgByMonth();
            break;
        case "5":
            setViewAvgBy8Hour();
            break;
    }
}

function setViewAvgByMinute() {
    $(".filter-hour").hide();
    $(".filter-8hour").hide();
    $(".filter-day").hide();
    $(".filter-month").hide();
    $(".filter-minute").show();
    $(".data-for-dt-hour").removeAttr('data-fordt');
    $(".data-for-dt-8hour").removeAttr('data-fordt');
    $(".data-for-dt-day").removeAttr('data-fordt');
    $(".data-for-dt-month").removeAttr('data-fordt');
    $(".data-for-dt-minute").attr('data-fordt', '0');
    $("#btnExportExcel").attr('data-params', 'station_id,from_date,to_date,duration,is_exceed,view_type,data_type,added_columns');
}

function setViewAvgByHour() {
    $(".filter-8hour").hide();
    $(".filter-day").hide();
    $(".filter-month").hide();
    $(".filter-minute").hide();
    $(".filter-hour").show();

    $(".data-for-dt-8hour").removeAttr('data-fordt');
    $(".data-for-dt-day").removeAttr('data-fordt');
    $(".data-for-dt-month").removeAttr('data-fordt');
    $(".data-for-dt-minute").removeAttr('data-fordt');
    $(".data-for-dt-hour").attr('data-fordt', '0');
    $("#btnExportExcel").attr('data-params', 'station_id,from_date,to_date,duration,is_exceed,view_type,data_type,added_columns');
}

function setViewAvgBy8Hour() {
    $(".filter-day").hide();
    $(".filter-month").hide();
    $(".filter-minute").hide();
    $(".filter-hour").hide();
    $(".filter-8hour").show();
    $(".data-for-dt-day").removeAttr('data-fordt');
    $(".data-for-dt-month").removeAttr('data-fordt');
    $(".data-for-dt-minute").removeAttr('data-fordt');
    $(".data-for-dt-hour").removeAttr('data-fordt');
    $(".data-for-dt-8hour").attr('data-fordt', '0');
    $("#btnExportExcel").attr('data-params', 'station_id,from_date,to_date,view_type,is_exceed,data_type,added_columns');
}

function setViewAvgByDay() {
    $(".filter-month").hide();
    $(".filter-minute").hide();
    $(".filter-hour").hide();
    $(".filter-8hour").hide();
    $(".filter-day").show();
    $(".data-for-dt-month").removeAttr('data-fordt');
    $(".data-for-dt-minute").removeAttr('data-fordt');
    $(".data-for-dt-hour").removeAttr('data-fordt');
    $(".data-for-dt-8hour").removeAttr('data-fordt');
    $(".data-for-dt-day").attr('data-fordt', '0');
    $("#btnExportExcel").attr('data-params', 'station_id,from_date,to_date,duration,is_exceed,view_type,data_type,added_columns');

}

function setViewAvgByMonth() {
    $(".filter-minute").hide();
    $(".filter-hour").hide();
    $(".filter-8hour").hide();
    $(".filter-day").hide();
    $(".filter-month").show();
    $(".data-for-dt-minute").removeAttr('data-fordt');
    $(".data-for-dt-hour").removeAttr('data-fordt');
    $(".data-for-dt-8hour").removeAttr('data-fordt');
    $(".data-for-dt-day").removeAttr('data-fordt');
    $(".data-for-dt-month").attr('data-fordt', '0');
    $("#btnExportExcel").attr('data-params', 'station_id,Month,Year,view_type,is_exceed,data_type,added_columns');
}
