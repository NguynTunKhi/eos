var isLoadDatatable = false;

$(document).ready(function () {
    $('#ncbbAddedColumns_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    $('#ncbbAddedStations_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    $('#nclose_modal_btn').click(function(){
        $('#nmodal-form').css('display','none');
        $("#table_detail > tbody").empty();
    })

    $('#nbtnExportExcel').on('click', function (e) {
         if (!validateTime2())    {
            e.preventDefault();
            return false;
        }
        if ($('#ndt0_from_date').val() == '' && $('#ndt0_to_date').val() == '') {
            var table = $('#ncustom_datatable_0').DataTable();

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
        if ($('#ndt0_from_date').val() == '' && $('#ndt0_to_date').val() != '') {
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
    $('body').on('click', '#ncheck_station', function (e) {
        if(e.target.checked){
            $('#ncbbAddedStations option').prop('selected', true);
            $('#ncbbAddedStations').trigger("change");
            $('#ncbbAddedStations').trigger('chosen:updated');

        } else {
            $('#ncbbAddedStations option:selected').removeAttr('selected');
            $('#ncbbAddedStations').trigger("change");
            $('#ncbbAddedStations').trigger('chosen:updated');
        }
    });
    $('body').on('click', '#ncheck', function (e) {
        if(e.target.checked){
            $('#ncbbAddedColumns option').prop('selected', true);
            $('#ncbbAddedColumns').trigger("change");
            $('#ncbbAddedColumns').trigger('chosen:updated');

        } else {
            $('#ncbbAddedColumns option:selected').removeAttr('selected');
            $('#ncbbAddedColumns').trigger("change");
            $('#ncbbAddedColumns').trigger('chosen:updated');
        }
    });

    $('body').on('click', '.btnCustomSearch', function (e) {
        time = new Date();
        date = new Date().toISOString().split("T")[0];

        if (!validateTime())    {
            e.preventDefault();
            return false;
        }
        $('#nbtnExportExcel').removeClass('hide');
        oTable[0].fnFilter();
        if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
    });

    $('#ncbbStationType').change(function () {
        var url = $(this).data('url');

        var area_ids = ""
        if ($('#ncbbAreas').val() !== null) {
            area_ids= $('#ncbbAreas').val().join(',')
        }
        app.postAjax({
            url: url,
            data: {
                type: $('#ncbbStationType').val(),
                province_id: $('#ncbbProvinceId').val(),
                area_ids: area_ids,
            },
            callback: function (res) {
                if (res.success) {
                    $('#ncbbAddedStations').html(res.html_2);
                    $('#ncbbAddedStations').trigger("change");
                    $('#ncbbAddedStations').trigger("chosen:updated");

                    $('#ncbbAddedColumns').html(res.html);
                    $('#ncbbAddedColumns').trigger("change");
                    $('#ncbbAddedColumns').trigger("chosen:updated");

                    $('#ncbbProvinceId').html(res.html3);
                    $('#ncbbProvinceId').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#ncbbStationId').val() == '') $('#nbtnExportExcel').addClass('hide');
    });

    $('#ncbbProvinceId').change(function () {
        var url = $(this).data('url');
        var area_ids = ""
        console.log($('#ncbbAreas').val())
        if ($('#ncbbAreas').val() !== null) {
            console.log("Heeee")
            area_ids= $('#ncbbAreas').val().join(',')
        }
        app.postAjax({
            url: url,
            data: {
                type: $('#ncbbStationType').val(),
                province_id: $('#ncbbProvinceId').val(),
                area_ids: area_ids,
            },
            callback: function (res) {
                if (res.success) {
                    $('#ncbbAddedStations').html(res.html_2);
                    $('#ncbbAddedStations').trigger("change");
                    $('#ncbbAddedStations').trigger("chosen:updated");

                    $('#ncbbAddedColumns').html(res.html);
                    $('#ncbbAddedColumns').trigger("change");
                    $('#ncbbAddedColumns').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#ncbbStationId').val() == '') $('#nbtnExportExcel').addClass('hide');
    });

    $('#ncbbAreas').change(function () {
        console.log("hello")
        var url = $(this).data('url');
        var area_ids = ""
        if ($('#ncbbAreas').val() !== null) {
            area_ids= $('#ncbbAreas').val().join(',')
        }
        app.postAjax({
            url: url,
            data: {
                type: $('#ncbbStationType').val(),
                province_id: $('#ncbbProvinceId').val(),
                area_ids: area_ids,
            },
            callback: function (res) {
                if (res.success) {
                    $('#ncbbAddedStations').html(res.html_2);
                    $('#ncbbAddedStations').trigger("change");
                    $('#ncbbAddedStations').trigger("chosen:updated");

                    $('#ncbbAddedColumns').html(res.html);
                    $('#ncbbAddedColumns').trigger("change");
                    $('#ncbbAddedColumns').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#ncbbStationId').val() == '') $('#nbtnExportExcel').addClass('hide');
    });

    $('#ndt0_to_date').val(new Date().toISOString().split("T")[0]);
    time = new Date($('#ndt0_to_date').val());
    time.setDate(time.getDate() - 30);
    date_min = time.toISOString().split("T")[0];
    $('#ndt0_from_date').val(date_min);
    if ($('#ncbbProvinceId').val()) {
        $('#ncbbProvinceId').trigger('change');
    }
    if ($('#ncbbStationId').val()) {
        isLoadDatatable = true;
        $('#ncbbStationId').trigger('change');
    } else {
        loadDataTableForPage();
    }
});
function validateTime2() {
    var dt0_from_date = $('#ndt0_from_date');
    var dt0_to_date = $('#ndt0_to_date');
    var fromDate = new Date(dt0_from_date.val());
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime( maxDate.getTime() + myTimeZone * 60 * 60 * 1000 );
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val() == '') {
        console.log("Datee")
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#ndt0_to_date').val(tempDate);
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
    var dt0_from_date = $('#ndt0_from_date');
    var dt0_to_date = $('#ndt0_to_date');
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
        $('#ndt0_to_date').val(tempDate);
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
        // $('#ndt0_to_date').val('');
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
        {'sWidth': '3%'},
        {'sWidth': '20%'},
    ];

    var aoClass = ['', 'text-left'];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
    return true;
}


function show_info(e){
    $('#nmodal-form').css('display','block')
    var url = $("#table_detail").attr("data-url");
    var from_date = $('#ndt0_from_date').val()
    var to_date = $('#ndt0_to_date').val()
    var station_id = $('#ncbbStationId').val()
    var data_type = $('#ndt0_data_type').val()
    var $table = $('#ntable_detail > tbody')
    $.ajax({
      type: "POST",
      url: url,
      data: {'indicator' : e , 'from_date': from_date, 'to_date' : to_date, 'station_id' : station_id, 'data_type' : data_type},
      success: function(rs) {
            if(rs.success) {
                html = ''
                for (var i = 0; i < rs.aaData.length; i++) {
                       idx = i + 1
                       html+= '<tr>' + '<td>' + idx +'</td>'
                       html+= '<td>' + rs.aaData[i][0] +'</td>'
                       html+= '<td>' + rs.aaData[i][1] +'</td>' + '</tr>'
                }
                $table.append(html)
            }
      }})
};

$(document).keyup(function(e) {
    if (e.keyCode == 27) {
        $('#nmodal-form').css('display','none');
        $("#table_detail > tbody").empty();
    }
});