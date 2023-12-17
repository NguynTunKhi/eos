var isLoadDatatable = false;

$(document).ready(function() {
    loadDataTableForPage();

    $('body').on('click', '.data_filter_by', function (e) {
        var items = $('.data_filter_by');
        var total = items.length;
        var data_filter_by = '';
        for(var i=0; i<total; i++){
            if($(items[i]).prop('checked')){
                if (data_filter_by){
                    data_filter_by += ';';
                }
                data_filter_by += $(items[i]).attr('data-value');
            }
        }
        $('#dt0_data_filter_by').val(data_filter_by);
    });

    $('body').on('change', '#dt0_data_type', function (e) {
        var currentValue = $(this).val();
        $('#btnReject').hide();
        $('#btnRemove').hide();
        $('#btnApprove').hide();
        if (currentValue == '1'){
            $('#btnApprove').show();
            $('#btnRemove').show();
        } else if (currentValue == '2'){
            $('#btnReject').show();
        }
        showHideMatrixCheckbox();
    });

    $('body').on('dblclick', '#custom_datatable_0 tbody td', function (e) {
        var adjustControl = $(this).find('.inline_adjust');
        if (adjustControl.length == 0){
            return false;
        }
        if (adjustControl.hasClass('active')){
            return false;
        }
        if ($('.inline_adjust.active').length > 0){
            return false;
        }
        adjustControl.addClass('active');
        adjustControl.show();
        $(this).find('span').hide();
        adjustControl.focus();
    });

    $('body').on('blur', '.inline_adjust', function (e) {
        var thisInstance = this;
        var id = $(this).attr('data-id');
        var new_value = $(this).val();
        var table = $(this).attr('data-table');
        var old_value = $(this).attr('data-oldValue');
        if (old_value != new_value){
            var params = {
                table: table,
                record_id: id,
                indicator: $(this).attr('data-indicator'),
                new_value: new_value,
            };
            var url = $('#hfUrlForInlineAdjust').val();
            app.showProgress();
            app.postAjax({
                url: url,
                showProgress: false,
                data: params,
                callback: function (res) {
                    app.hideProgress();
                    oTable[0].fnFilter('');
                }
            });
        } else {
            oTable[0].fnFilter('');
        }
    });

    $('body').on('keyup', '.inline_adjust', function (e) {
        return true; // Todo: Enter to search
        if(e.keyCode == 13){
            var thisInstance = this;
            var id = $(this).attr('data-id');
            var new_value = $(this).val();
            var table = $(this).attr('data-table');
            var old_value = $(this).attr('data-oldValue');
            if (old_value != new_value){
                var params = {
                    table: table,
                    record_id: id,
                    indicator: $(this).attr('data-indicator'),
                    new_value: new_value,
                };
                var url = $('#hfUrlForInlineAdjust').val();
                app.showProgress();
                app.postAjax({
                    url: url,
                    showProgress: false,
                    data: params,
                    callback: function (res) {
                        app.hideProgress();
                        oTable[0].fnFilter('');
                    }
                });
            } else {
                oTable[0].fnFilter('');
            }
        }
    });

    $('body').on('change', '#dt0_area_id, #dt0_station_type, #dt0_province_id', function (e) {
        var url = $(this).data('url');
        var area_id = $('#dt0_area_id').val();
        var station_type = $('#dt0_station_type').val();
        var province_id = $('#dt0_province_id').val();
        var data = {
            area_id: area_id,
            province_id: province_id,
            station_type: station_type,
        };
        app.postAjax({
            url: url,
            data: data,
            callback: function (res) {
                if (res.success) {
                    $('#dt0_station_id').html(res.html);
                    $('#dt0_station_id').trigger("chosen:updated");
                }
            }
        });
    });

    $('#dt0_station_id').change(function() {
        var url = $(this).data('url');
        var station_id = $('#dt0_station_id').val();
        app.postAjax({
            url: url,
            data: {station_id : station_id},
            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedColumns').html(res.html);
                    $('#cbbAddedColumns').trigger("change");
                    $('#cbbAddedColumns').trigger("chosen:updated");
                    if (isLoadDatatable){
                        loadDataTableForPage();
                        isLoadDatatable = false;
                        $('.btnSearch').trigger('click');
                    }
                } else {
                    app.showError(res.message);
                }
            }
        });

        if (station_id){
            $('body').find('.tab-chart').trigger('click');
        }
    });

    $('body').on('click', '.btnSearch', function (e) {
        if (!$('#dt0_station_id').val()){
            e.preventDefault();
            app.showError(app.translate('Please select a station first!'));
            return false;
        }
    });

    $('body').off('click', '.tab-chart');
    $('body').on('click', '.tab-chart', function (e) {
        if (!$('#dt0_station_id').val()){
            e.preventDefault();
            app.showError(app.translate('Please select a station first!'));
            return false;
        }
        var container = $('#tab_qa_qc_chart');
        var station_id = $('#dt0_station_id').val();
        if (station_id) {
            var url = container.attr('data-url');
            url += '?' + $.param({station_id: station_id});
            container.load(url);
        } else {
            container.html('');
        }
    });

    $('body').off('click', '.tab-list');
    $('body').on('click', '.tab-list', function (e) {
        $('.btnSearch').trigger('click');
    });
    
    $('body').off('click', '#btnApprove, #btnRemove');
    $('body').on('click', '#btnApprove, #btnRemove', function (e) {
        var items = $('.row_item:checked');
        if (items.length == 0){
            app.showError(app.translate('MSG_SELECT_ATLEAST_ONE_RECORD'));
            return true;
        }
        var messageConfirm = $(this).attr('data-confirm');
        var url = $(this).attr('data-url');
        var data = {};
        for (var i=0; i<items.length; i++){
            var ele = $(items[i]).closest('td').find('.inline_adjust');
            var id = ele.attr('data-id');
            var indicator = ele.attr('data-indicator');
            if (data[id] == undefined){
                data[id] = '';
            }
            if (data[id]){
                data[id] += ';';
            }
            data[id] += indicator;
        }
        data = JSON.stringify(data);
        app.showConfirmBox({
            content: messageConfirm,
            callback: function () {
                app.postAjax({
                    url: url,
                    data: {data: data},
                    callback: function (data) {
                        toastr['success'](app.translate('JS_MSG_SAVE_SUCCESS'));
                        oTable[0].fnDraw();
                    }
                });
            },
        });
    });

    $('body').find( '#dt0_data_type').trigger('change');

    showHideMatrixCheckbox();
});

function showHideMatrixCheckbox() {
    if ($('#dt0_data_type').val() == '1'){ // CHUA KIEM DUYET
        $('.column_all').show();
    } else {
        $('.column_all').hide();
    }
    $('.select_row_all').show();
}

function loadDataTableForPage() {
    var aoColumns = [
        {'sWidth' : '2%'},
        {'sWidth' : '2%'},
        {'sWidth' : '25%'},
        {'sWidth' : '18%'},
    ];

    var aoClass = ['', '', 'text-left'];
    var sDom = "<'row horizontal-scroll't><'clear'><'row bottom' <'col-sm-6 text-left' li><'col-sm-6 text-right' p>><'clear'>";
    loadDataTable({
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
    });
    
    return true;
}