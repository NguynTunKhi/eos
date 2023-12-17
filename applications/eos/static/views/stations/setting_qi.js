$(document).ready(function () {
    loadDataTableForPage();

    $('body').on('change', '#station_id', function (e) {
        oTable[0].fnFilter();
    });

    $('body').on('change', '#station_type', function (e) {
        oTable[0].fnFilter();
    });

    $('body').on('click', '#btnSave', function (e) {
        var url = $(this).data('url');
        var checked = '';
        var unchecked = '';
        var items = $("#custom_datatable_0 tbody tr");
        var total = items.length;
        var station_names = '';

        station_public = '';
        station_unpublic = '';
        var arrayCalcAqi = ['PM-10', 'PM-2-5'];
        for (var i = 0; i < total; i++) {
            var item = $(items[i]);
            if (item.find('input').length == 0) {
                continue;
            }
            var station_id = item.find('label.check_public').first().attr('data-station');
            var station_name = item.find("td").eq(1).html();
            var items_indicator = item.find('input');
            var total_indicator = items_indicator.length;
            // Check thong so cho phep tinh AQI
            var isArrayCalcAqi = false;
            if (item.find('input:checked').length >= 1) {
                for (var k = 0; k < total_indicator; k++) {
                    var item_indicator = item.find(items_indicator[k]);
                    var item_indicator_name = $(items_indicator[k]).attr('data_indicator');
                    if (item_indicator.prop('checked')) {
                        if (arrayCalcAqi.indexOf(item_indicator_name) !== -1) {
                            isArrayCalcAqi = true;
                        }
                    }
                }
            }
            if (item.find('input:checked').length >= 1 && isArrayCalcAqi) {
                if (station_public) {
                    station_public += ',';
                }
                station_public += station_id;
                for (var j = 0; j < total_indicator; j++) {
                    var item_indicator = item.find(items_indicator[j]);
                    var item_indicator_name = $(items_indicator[j]).attr('data_indicator');

                    if (item_indicator.prop('checked')) {
                        if (checked) {
                            checked += ',';
                        }
                        checked += $(items_indicator[j]).attr('id');
                    } else {
                        if (unchecked) {
                            unchecked += ',';
                        }
                        unchecked += $(items_indicator[j]).attr('id');
                    }
                }
            }
            if (isArrayCalcAqi == false) {
                    station_names += '- ' + station_name + '</br>';
            }
        }
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function () {
                params = {
                    checked: checked,
                    unchecked: unchecked,
                    station_public: station_public,
                    station_unpublic: station_unpublic,
                };

                app.postAjax({
                    url: url,
                    showProgress: false,
                    data: params,
                    callback: function (res) {
                        if (res.success) {
                            if (station_names != '') {
                                toastr['warning']('<h5>Các trạm sau chưa cập nhật - Phương pháp tính VN_AQI yêu cầu bắt buộc phải có tối thiểu một trong hai thông số [PM-10, PM-2-5]: </h5>' + station_names);
                            }
                            if ((checked != '')) {
                                toastr['success'](app.translate('JS_MSG_SAVE_SUCCESS'));
                            }
                            oTable[0].fnFilter();
                        }
                    }
                });
            }
        });

    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth': '5%'},
        {'sWidth': '20%'},
        {'sWidth': '75%'},
    ];

    var aoClass = ['', 'text-left', 'text-left'];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,

    });

    return true;
}

