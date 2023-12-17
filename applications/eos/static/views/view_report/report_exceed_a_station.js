var isLoadDatatable = false;

$(document).ready(function () {
    $('#ecbbAreas_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    $('#ecbbAddedColumns_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    $('#ecbbAddedStations_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    $('#eclose_modal_btn').click(function(){
        $('#emodal-form').css('display','none');
        $("#etable_detail > tbody").empty();
    })


    $('#ebtnExportExcelCommonFile').on('click', function (e) {
        if (!validateTime2())    {
           e.preventDefault();
           return false;
       }
       if ($('#edt0_from_date').val() == '' && $('#edt0_to_date').val() == '') {
           var table = $('#ecustom_datatable_0').DataTable();

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
       if ($('#edt0_from_date').val() == '' && $('#edt0_to_date').val() != '') {
           e.preventDefault();
           app.showError(app.translate('ERR_Day_Blank'));
           return false;
       }
       var url = $(this).attr("data-url");
           var allParams = $(this).attr("data-params").split(",");
           var params = {
               'sSearch': $("#ecustom_datatable_0_filter input").val()
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
       console.log("urllllllllll",url)
           window.open(url);
   });

    $('body').on('click', '#echeck_station', function (e) {
        if(e.target.checked){
            $('#ecbbAddedStations option').prop('selected', true);
            $('#ecbbAddedStations').trigger("change");
            $('#ecbbAddedStations').trigger('chosen:updated');

        } else {
            $('#ecbbAddedStations option:selected').removeAttr('selected');
            $('#ecbbAddedStations').trigger("change");
            $('#ecbbAddedStations').trigger('chosen:updated');
        }
    });
    $('body').on('click', '#echeck', function (e) {
        if(e.target.checked){
            $('#ecbbAddedColumns option').prop('selected', true);
            $('#ecbbAddedColumns').trigger("change");
            $('#ecbbAddedColumns').trigger('chosen:updated');

        } else {
            $('#ecbbAddedColumns option:selected').removeAttr('selected');
            $('#ecbbAddedColumns').trigger("change");
            $('#ecbbAddedColumns').trigger('chosen:updated');
        }
    });

    $('body').on('click', '#btnCustomSearch', function (e) {
        time = new Date();
        date = new Date().toISOString().split("T")[0];

        if (!validateTime())    {
            e.preventDefault();
            return false;
        }
        if (!$('#ecbbAddedColumns').val()) {
            e.preventDefault();
            app.showNotification({"content": app.translate('Please select indicator first!')});
            return false;
        }
        $('#ebtnExportExcel').removeClass('hide');
        $('#ebtnExportExcelCommonFile').removeClass('hide');
        oTable[0].fnFilter();
        if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
    });

    $('#ecbbStationType').change(function () {
        var url = $(this).data('url');
        let area_ids = ""
        if ($('#ecbbAreas').val() !== null) {
            area_ids= $('#ecbbAreas').val().join(',')
        }
        app.postAjax({
            url: url,
            data: {type: $('#ecbbStationType').val(),
                province_id: $('#ecbbProvinceId').val(),
                area_ids: area_ids
            },
            callback: function (res) {
                if (res.success) {
                    $('#ecbbAddedStations').html(res.html_2);
                    $('#ecbbAddedStations').trigger("change");
                    $('#ecbbAddedStations').trigger("chosen:updated");

                    $('#ecbbAddedColumns').html(res.html);
                    $('#ecbbAddedColumns').trigger("change");
                    $('#ecbbAddedColumns').trigger("chosen:updated");

                    $('#ecbbProvinceId').html(res.html3);
                    $('#ecbbProvinceId').trigger("chosen:updated");

                    $('#ecbbAddAreas').html(res.html5);
                    $('#ecbbAddAreas').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#ecbbStationId').val() == '') $('#ebtnExportExcel').addClass('hide');
    });

    $('#ecbbProvinceId').change(function () {
        var url = $(this).data('url');
        let area_ids = ""
        if ($('#ecbbAreas').val() !== null) {
            area_ids= $('#ecbbAreas').val().join(',')
        }

        app.postAjax({
            url: url,
            data: {
                type: $('#ecbbStationType').val(),
                province_id: $('#ecbbProvinceId').val(),
                area_ids: area_ids,
            },
            callback: function (res) {
                if (res.success) {
                    $('#ecbbAddedStations').html(res.html_2);
                    $('#ecbbAddedStations').trigger("change");
                    $('#ecbbAddedStations').trigger("chosen:updated");

                    $('#ecbbAddedColumns').html(res.html);
                    $('#ecbbAddedColumns').trigger("change");
                    $('#ecbbAddedColumns').trigger("chosen:updated");

                    $('#ecbbAddAreas').html(res.html5);
                    $('#ecbbAddAreas').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#ecbbStationId').val() == '') $('#ebtnExportExcel').addClass('hide');
    });

    $('#ecbbAreas').change(function () {
        var url = $(this).data('url');
        let area_ids = ""
        if ($('#ecbbAreas').val() !== null) {
            area_ids= $('#ecbbAreas').val().join(',')
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
                    $('#ecbbAddedStations').html(res.html_2);
                    $('#ecbbAddedStations').trigger("change");
                    $('#ecbbAddedStations').trigger("chosen:updated");

                    $('#ecbbAddedColumns').html(res.html);
                    $('#ecbbAddedColumns').trigger("change");
                    $('#ecbbAddedColumns').trigger("chosen:updated");

                    $('#ecbbAddAreas').html(res.html5);
                    $('#ecbbAddAreas').trigger("chosen:updated");

                    if (isLoadDatatable) {
                        loadDataTableForPage();
                        isLoadDatatable = false;
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if ($('#ecbbStationId').val() == '') $('#ebtnExportExcel').addClass('hide');
    });


    $('#edt0_to_date').val(new Date().toISOString().split("T")[0]);
    time = new Date($('#edt0_to_date').val());
    time.setDate(time.getDate() - 30);
    date_min = time.toISOString().split("T")[0];
    $('#edt0_from_date').val(date_min);
    if ($('#ecbbProvinceId').val()) {
        $('#ecbbProvinceId').trigger('change');
    }
    if ($('#ecbbStationId').val()) {
        isLoadDatatable = true;
        $('#ecbbStationId').trigger('change');
    } else {
        loadDataTableForPage();
    }
});
function validateTime2() {
    var dt0_from_date = $('#edt0_from_date');
    var dt0_to_date = $('#edt0_to_date');
    var fromDate = new Date(dt0_from_date.val());
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime( maxDate.getTime() + myTimeZone * 60 * 60 * 1000 );
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val()=='')    {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#edt0_to_date').val(tempDate);
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
    var dt0_from_date = $('#edt0_from_date');
    var dt0_to_date = $('#edt0_to_date');
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
        $('#edt0_to_date').val(tempDate);
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
        // $('#edt0_to_date').val('');
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
    $('#emodal-form').css('display','block')
    var url = $("#etable_detail").attr("data-url");
    var from_date = $('#edt0_from_date').val()
    var to_date = $('#edt0_to_date').val()
    var station_id = $('#ecbbStationId').val()
    var data_type = $('#edt0_data_type').val()
    var $table = $('#etable_detail > tbody')
    
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
        $('#emodal-form').css('display','none');
        $("#etable_detail > tbody").empty();
    }
});