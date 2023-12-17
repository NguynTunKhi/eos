$(document).ready(function() {
    loadDataTableForPage();
    
    $('body').on('change', '#station_id', function (e) {
        oTable[0].fnFilter();
    });

    $('body').on('change', '#station_type', function (e) {
        oTable[0].fnFilter();
    });

    $('body').on('change', '#is_public', function (e) {
        oTable[0].fnFilter();
    });
    
    $('body').on('click', '#btnSave', function (e) {
        var url = $(this).data('url');
        var items = $('label.check_public input');
        var total = items.length;
        var checked = '';
        var unchecked = '';
        for (var i=0; i<total; i++){
            var item = $(items[i]);
            if (item.prop('checked')) {
                if (checked) {
                    checked += ',';
                }
                checked += $(items[i]).attr('id');
            } else {
                if (unchecked) {
                    unchecked += ',';
                }
                unchecked += $(items[i]).attr('id');
            }
        }
        items = $("#custom_datatable_0 tbody tr");
        var total = items.length;
        station_public = ''
        station_unpublic = ''
        station_data_type = ''
        for (var i=0; i<total; i++){
            var item = $(items[i]);
            if (item.find('input').length == 0){
                continue;
            }
            var station_id = item.find('label.check_public').first().attr('data-station');
            if (item.find('input:checked').length > 1){
                if (station_public){
                    station_public += ',';
                }
                station_public += station_id;
            } else {
                if (station_unpublic){
                    station_unpublic += ',';
                }
                station_unpublic += station_id;
            }


            if (station_data_type){
                station_data_type += ',';
            }
            var radioValue = $('input[name='+station_id+']:checked').val();
            station_data_type += station_id + "_" + radioValue;
        }

        var item_data_type = $('label.data_type input');

        // Check for show station style on menu
        var station_style_0 = 0;
        if ($('#station_style_0').is(":checked")) {
            station_style_0 = 1;
        }
        var station_style_1 = 0;
        if ($('#station_style_1').is(":checked")) {
            station_style_1 = 1;
        }
        var station_style_3 = 0;
        if ($('#station_style_3').is(":checked")) {
            station_style_3 = 1;
        }
        var station_style_4 = 0;
        if ($('#station_style_4').is(":checked")) {
            station_style_4 = 1;
        }

        // Check for public statsions
        var is_publics = $('label.is_public input');
        var total = is_publics.length;
        var is_publics_checked = '';
        var is_publics_unchecked = '';
        for (var i=0; i<total; i++){
            var item = $(is_publics[i]);
            if (item.prop('checked')) {
                if (is_publics_checked) {
                    is_publics_checked += ',';
                }
                is_publics_checked += $(is_publics[i]).attr('id');
            } else {
                if (is_publics_unchecked) {
                    is_publics_unchecked += ',';
                }
                is_publics_unchecked += $(is_publics[i]).attr('id');
            }
        }

        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function() {
                params = {
                    checked: checked,
                    unchecked: unchecked,
                    station_public: station_public,
                    station_unpublic: station_unpublic,
                    station_data_type: station_data_type,
                    station_style_0: station_style_0,
                    station_style_1: station_style_1,
                    station_style_3: station_style_3,
                    station_style_4: station_style_4,
                    is_publics_checked: is_publics_checked,
                    is_publics_unchecked: is_publics_unchecked
                };
                
                app.postAjax({
                    url: url,
                    showProgress: false,
                    data: params,
                    callback: function (res) {
                        if (res.success){
                            toastr['success'](app.translate('JS_MSG_SAVE_SUCCESS'));
                        }
                    }
                });
            }
        });
        
    });

    $('#station_type').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {filter_value: $(this).val()+ ';' + true},

            callback: function (res) {
                if (res.success) {
                    $('#station_id').html(res.html);
                    $('#station_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%'},
        {'sWidth' : '10%'},
        {'sWidth' : '20%'},
        {'sWidth' : '10%'},
        {'sWidth' : '55%'},
    ];

    var aoClass = ['', 'text-center', 'text-left', 'text-left', 'text-left'];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,

    });

    return true;
}