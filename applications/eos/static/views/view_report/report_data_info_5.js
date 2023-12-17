var isLoadDatatable = false;
function setLoading() {
    var loadingIcon = $('#hfLoadingIcon').val();
    $("#wrapper").block({
            blockMsgClass: 'blockOnDiv',
            message:   'Đang xử lý <img style="width: 25px; height: 25px;" src="' + loadingIcon + '" />'
    });
}
function disableLoading() {
    $("#wrapper").unblock();
    $("#lll").attr("ticketid", "");
    $('#fa-spin-process').addClass('hide');
    $('.btnCustomSearch').removeClass('hide');
}
$(document).ready(function () {
    $('#cbbAddedColumns_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    $('#cbbAddedStations_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')

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

    $('body').on('click', '.btnCustomSearch', function (e) {
        time = new Date();
        date = new Date().toISOString().split("T")[0];
        if ($('#cbbDuration').length > 0) {
            time.setDate(time.getDate() - $('#cbbDuration option:selected').val());
            var date_change = new Date(time).toISOString().split("T")[0];
        }

        if (!$('#cbbStationType').val())
        {
            e.preventDefault();
            app.showError(app.translate('Please select a station type!'));
            return false;
        }
        if (!validateTime())    {
            e.preventDefault();
            return false;
        }
        $('#btnExportExcel').removeClass('hide');
        $('#fa-spin-process').removeClass('hide');
        $('.btnCustomSearch').addClass('hide');
        // oTable[0].fnFilter();
        // if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
        setLoading();
        loadDataTableForPageAndCreateTicket();
    });

    $('#cbbStationType').change(function () {
        var url = $(this).data('url');
        let area_ids = ""
        if ($('#cbbAreas').val() !== null) {
            area_ids= $('#cbbAreas').val().join(',')
        }

         var careers = "";
        if ($("#cbbCareer").val() !== null) {
            careers = $("#cbbCareer").val().join(",")
        }

        app.postAjax({
            url: url,
            data: {
                type: $('#cbbStationType').val(),
                province_id: $('#cbbProvinceId').val(),
                area_ids: area_ids,
                careers: careers,
            },
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedStations').html(res.html_2);
                    $('#cbbAddedStations').trigger("change");
                    $('#cbbAddedStations').trigger("chosen:updated");

                    $('#cbbAddedColumns').html(res.html);
                    $('#cbbAddedColumns').trigger("change");
                    $('#cbbAddedColumns').trigger("chosen:updated");

                    $('#cbbProvinceId').html(res.html3);
                    $('#cbbProvinceId').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        // loadDataTableForPage();
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
         var careers = "";
        if ($("#cbbCareer").val() !== null) {
            careers = $("#cbbCareer").val().join(",")
        }

         let area_ids = ""
        if ($('#cbbAreas').val() !== null) {
            area_ids= $('#cbbAreas').val().join(',')
        }

        app.postAjax({
            url: url,
            data: {
                type: $('#cbbStationType').val(),
                province_id: $('#cbbProvinceId').val(),
                careers: careers,
                area_ids:area_ids
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

    $('#cbbAreas').change(function () {
        var url = $(this).data('url');
         let area_ids = ""
        if ($('#cbbAreas').val() !== null) {
            area_ids= $('#cbbAreas').val().join(',')
        }

        var careers = "";
        if ($("#cbbCareer").val() !== null) {
            careers = $("#cbbCareer").val().join(",")
        }

        app.postAjax({
            url: url,
            data: {
                type: $('#cbbStationType').val(),
                province_id: $('#cbbProvinceId').val(),
                area_ids: area_ids,
                careers:careers,
            },
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedStations').html(res.html_2);
                    $('#cbbAddedStations').trigger("change");
                    $('#cbbAddedStations').trigger("chosen:updated");

                    $('#cbbAddedColumns').html(res.html);
                    $('#cbbAddedColumns').trigger("change");
                    $('#cbbAddedColumns').trigger("chosen:updated");

                    $('#cbbProvinceId').html(res.html3);
                    $('#cbbProvinceId').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        // loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#cbbStationId').val() == '') $('#btnExportExcel').addClass('hide');
    });



    $('#cbbProvinceId').change(function () {
        var url = $(this).data('url');
         let area_ids = ""
        if ($('#cbbAreas').val() !== null) {
            area_ids= $('#cbbAreas').val().join(',')
        }
        app.postAjax({
            url: url,
            data: {
                type: $('#cbbStationType').val(),
                province_id: $('#cbbProvinceId').val(),
                area_ids: area_ids,
            },
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedStations').html(res.html_2);
                    $('#cbbAddedStations').trigger("change");
                    $('#cbbAddedStations').trigger("chosen:updated");

                    $('#cbbAddedColumns').html(res.html);
                    $('#cbbAddedColumns').trigger("change");
                    $('#cbbAddedColumns').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        // loadDataTableForPage();
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
        // loadDataTableForPage();
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


function intervalCheckResult(data) {
            if (data.ticketID) {
                $("#lll").attr("ticketid", data.ticketID);
                console.log($("#ticket_id"))
                $("#ticket_id").val( data.ticketID);
                let result = true;
                let idInterval = setInterval(loadTicketDataAndBindDatatable, 2000);
                setTimeout(function(){
                    clearInterval(idInterval);
                    disableLoading();
                },300000);
                function loadTicketDataAndBindDatatable() {
                    result = loadDataTableForPage2(data.ticketID, data.total_stations);
                    if (!result) {
                        clearInterval(idInterval);
                    }
                }
            } else {
                app.showError(data.message);
                disableLoading();
            }
        }
function loadDataTableForPageAndCreateTicket() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth': '3%'},
        {'sWidth': '20%'},
        {'sWidth': '20%'},
        {'sWidth': '20%'},
    ];
    var aoClass = ['', '', ''];
    loadDataTable({
        doNotShowProgress: true,
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomCallback: intervalCheckResult,
    });
    return true;
}

// function loadDataTableForPage() {
//     var sAjaxSource = $("#custom_datatable_0").attr("data-url");
//     var aoColumns = [
//         {'sWidth': '3%'},
//         {'sWidth': '20%'},
//         {'sWidth': '20%'},
//         {'sWidth': '20%'},
//     ];
//
//     var aoClass = ['', '', ''];
//     loadDataTable({
//         sAjaxSource: sAjaxSource,
//         aoColumns: aoColumns,
//         aoClass: aoClass,
//     });
//     return true;
// }

function loadDataTableForPage2(ticketID, total_stations) {
    var url = $("#hfUrlget_list_report_data_info_5_in_ticket_report").val();
    var ticketid = $("#lll").attr("ticketid");
    if (ticketid === "") {
        return false;
    }
    var aoColumns = [
        {'sWidth': '3%'},
        {'sWidth': '20%'},
        {'sWidth': '20%'},
        {'sWidth': '20%'},
    ];

    var aoClass = ['', '', ''];
    loadDataTable({
        sAjaxSource: url,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomAoData: function (aoData) {
            aoData.push({
				"name": "ticketid", "value": ticketID,
			});
            aoData.push({
				"name": "total_stations", "value": total_stations,
			});
        },
        fnCustomCallback: function (data) {
            if (!data.success || (data.status && data.status == "DONE")) {
                disableLoading();
            }
        },
        fnDeferInjectDataToTable: function () {
            $(".bottom").hide();
        },
        doNotShowProgress: true,
    });
    return true;
}

