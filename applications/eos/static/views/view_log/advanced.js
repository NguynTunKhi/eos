var isLoadDatatable = false;

$(document).ready(function () {
    $('#cbbAddedStations_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')

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

    $('#cbbStationType, #cbbProvinceId').change(function () {
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

                    $('#cbbIndicatorId').html(res.html);
                    $('#cbbIndicatorId').trigger("chosen:updated");

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

    $('body').on('click', '.btnCustomSearch', function (e) {
        var sSource = $("#custom_datatable_advanced").attr("data-url");
        var station_type = $('#cbbStationType').val()
        var province_id = $('#cbbProvinceId').val()
        var indicator_id = $('#cbbIndicatorId').val()
        var from_date = $('#dt0_from_date').val()
        var to_date = $('#dt0_to_date').val()
        var data_type = $('#dt0_data_type').val()
        var add_stations = $('#cbbAddedStations').val().toString()
        var view_type = $('#dt0_view_type').val()

        var $table = $('#custom_datatable_advanced')
        var $body = $('#custom_datatable_advanced > tbody')
        var $header =  $('#custom_datatable_advanced > thead')
        $body.empty()
        $header.empty()
        $.ajax({
            "dataType": 'json',
            "type": "POST",
            "url": sSource,
            "data": {station_type : station_type,
                     province_id : province_id,
                     indicator_id : indicator_id,
                     from_date : from_date,
                     to_date : to_date,
                     data_type : data_type,
                     add_stations : add_stations,
                     view_type: view_type
                     },
            "success": function(rs) {
                html_header = '<tr>' +  '<th style = "width: 5%;">' + '#' + '</th>' + '<th style = "width: 15%;">' + 'Ngày giờ' + '</th>'
                if(rs.success) {
                    if(rs.aaData.length > 0){
                        for (var i = 0; i < rs.station_name.length; i++) {
                        html_header+= '<th>' + rs.station_name[i] +'</th>'
                        }
                        $header.append(html_header)
                        $header.append('</tr>')
                        html_body = ''
                        for (var i = 0; i < rs.aaData.length; i++) {
                           idx = i + 1
                           html_body+= '<tr>' + '<td>' + idx +'</td>'
                           for (var j = 0; j < rs.aaData[i].length; j++) {
                                html_body+= '<td>' + rs.aaData[i][j] +'</td>'
                           }
                           html_body+= '</tr>'
                        }
                        $body.append(html_body)
                    }
                    else{
                        for (var i = 0; i < rs.station_name.length; i++) {
                            html_header+= '<th>' + rs.station_name[i] +'</th>'
                        }
                        $header.append(html_header)
                        $header.append('</tr>')
                        col = rs.station_name.length + 2
                        html_no_data = '<tr class = "odd">' + '<td valign = "top" colspan =' + col + '>' + 'Không có dữ liệu!'+ '</td>' + '</tr>'
                        $body.append(html_no_data)
                    }
                }
            },
        });
    });

    $('#dt0_to_date').val(new Date().toISOString().split("T")[0]);
    time = new Date($('#dt0_to_date').val());
    time.setDate(time.getDate() - 30);
    date_min = time.toISOString().split("T")[0];
    $('#dt0_from_date').val(date_min);
    if ($('#cbbProvinceId').val()) {
        $('#cbbProvinceId').trigger('change');
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

