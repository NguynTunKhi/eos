$(document).ready(function () {
    $('#indicator_multi_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')

    $('#btnExportExcel').on('click', function (e) {
        if ($('#dt0_from_date').val() == '' && $('#dt0_to_date').val() == '') {
            var table = $('#custom_datatable_0').DataTable();

            data = table
                .rows()
                .data();
            column = table.column(1).data();
            time_temp = column[0].split(' ').reverse()[0].split('/').reverse().join('-') + ' ' + column[0].split(' ').reverse()[1];
            time_export = new Date().getTime() - new Date(time_temp).getTime();
            month_export = new Date(time_export).getMonth()+1;
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
                'sSearch': $("#custom_datatable_0_filter input").val(),
                'indicators': $('#indicator-multi').val().toString()
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


    $('body').on('click', '.btnCustomSearch', function (e) {
        if (!$('#station').val()) {
            e.preventDefault();
            app.showError(app.translate('Please select a station first!'));
            return false;
        }
        $('#btnExportExcel').removeClass('hide');
        if (!oTable[0]) {
            load_data_for_page()
        } else {
            oTable[0].fnFilter('');
        }
    });

    $('#station').change(function(){
        fetchIndicator($(this).val());
    })

    $('#station-type, #province').change(function () {
        var url = $(this).data('url');
        app.postAjax({
                url: url,
                data: {filter_value: $('#station-type').val().trim() + ';' + $('#province').val().trim()},
                callback: function (res) {
                    if (res.success) {
                        $('#station').html(res.html);
                        $('#station').trigger("chosen:updated");
                    } else {
                        app.showError(res.message);
                    }
                }
            });
        });

    $('#check').click(function(e){
         if(e.target.checked){
            $('#indicator-multi option').prop('selected', true);
            $('#indicator-multi').trigger("change");
            $('#indicator-multi').trigger('chosen:updated');
            } else {
            $('#indicator-multi option:selected').removeAttr('selected');
            $('#indicator-multi').trigger("change");
            $('#indicator-multi').trigger('chosen:updated');
            }
        });
    $('#to-date').val(new Date().toISOString().split("T")[0]);
    time = new Date($('#to-date').val());
    time.setDate(time.getDate() - 30);
    date_min = time.toISOString().split("T")[0];
    $('#from-date').val(date_min);
    if ($('#cbbStationId').val()) {
        isLoadDatatable = true;
        $('#cbbStationId').trigger('change');
    } else {
        load_data_for_page();
    }
})

function getParamsSearch(){
    var params_search = {};
    params_search['station_id'] = $('#station').val();
    params_search['station_type'] = Number($('#station-type').val());
    params_search['province_id'] = $('#province').val();
    params_search['from_date'] = $('#from-date').val();
    params_search['to_date'] = $('#to-date').val();
    params_search['discontinuity_type'] = $('#discontinuity-type').val();
    params_search['indicator_array'] = $('#indicator-multi').val().join(';');
    fetchData(params_search)
}

function fetchIndicator(station_id){
    url = $('#station').attr('data-url')
    app.postAjax({
        type:'POST',
        url: url,
        data:{station_id},
        callback: function(res){
        if(res.success){
            $('#indicator-multi').html(res.html);
            $('#indicator-multi').trigger("change");
            $('#indicator-multi').trigger("chosen:updated");
        }
    }
    })
}

function fetchData(params_search){
    url = $('#search-btn').attr('data-url')
    formatData()
}

function load_data_for_page(){
    var url = $('#custom_datatable_0').attr('data-url');
    var aoColumns = [
        {'sWidth' : '10%', 'bSortable' : false},
        {'sWidth' : '10%'},
        {'sWidth' : '20%'},
        {'sWidth' : '20%'},
        {'sWidth' : '20%'},
        {'sWidth' : '20%'}
    ];
    var aoClass = ['', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: url,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({'name': 'indicators', 'value': $('#indicator-multi').val()})
        }
    });
    return true;
}

