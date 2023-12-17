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
        var arrayCalcWqi_1 = ['pH', 'AS', 'Cd', 'Pb', 'Cr6+', 'Cu', 'Zn', 'Hg'];
        var arrayCalcWqi_2 = ['DO', 'BOD', 'COD', 'TOC', 'N-NH4', 'NO3', 'TN', 'P-PO4', 'TP'];
        var arrayCalcWqi_3 = ['TURBIDITY', 'TSS'];
        var arrayCalcWqi_4 = ['COLIFORM'];
        for (var i = 0; i < total; i++) {
            var item = $(items[i]);
            if (item.find('input').length == 0) {
                continue;
            }
            var station_id = item.find('label.check_public').first().attr('data-station');
            var station_name = item.find("td").eq(1).html();

            if (item.find('input:checked').length > 0) {
                if (station_public) {
                    station_public += ',';
                }
                station_public += station_id;

                var items_indicator = item.find('input');
                var total_indicator = items_indicator.length;

                var countExitInIndicatorAqi = 0;
                var countGroupCalWqi = 0;
                var countCalWqi_1 = 0;
                var countCalWqi_2 = 0;
                var countCalWqi_3 = 0;
                var countCalWqi_4 = 0;

                for (var j = 0; j < total_indicator; j++) {
                    var item_indicator = item.find(items_indicator[j]);
                    var item_indicator_name = $(items_indicator[j]).attr('data_indicator');

                    if (item_indicator.prop('checked')) {
                        // if (checked) {
                        //     checked += ',';
                        // }
                        // checked += $(items_indicator[j]).attr('id');
                        if (arrayCalcWqi_1.indexOf(item_indicator_name) !== -1) {
                            countCalWqi_1 = countCalWqi_1 + 1;
                            if (countCalWqi_1 == 1) {
                                countGroupCalWqi = countGroupCalWqi + 1;
                            }
                        }

                        if (arrayCalcWqi_2.indexOf(item_indicator_name) !== -1) {
                            countCalWqi_2 = countCalWqi_2 + 1;
                            if (countCalWqi_2 == 1) {
                                countGroupCalWqi = countGroupCalWqi + 1;
                            }
                        }

                        if (arrayCalcWqi_3.indexOf(item_indicator_name) !== -1) {
                            countCalWqi_3 = countCalWqi_3 + 1;
                            if (countCalWqi_3 == 1) {
                                countGroupCalWqi = countGroupCalWqi + 1;
                            }
                        }

                        if (arrayCalcWqi_4.indexOf(item_indicator_name) !== -1) {
                            countCalWqi_4 = countCalWqi_4 + 1;
                            if (countCalWqi_4 == 1) {
                                countGroupCalWqi = countGroupCalWqi + 1;
                            }
                        }
                    } else {
                        // if (unchecked) {
                        //     unchecked += ',';
                        // }
                        // unchecked += $(items_indicator[j]).attr('id');
                    }
                }

                if ((countCalWqi_2 < 1) || (countGroupCalWqi < 2)) {
                    station_names += '- ' + station_name + '</br>';
                } else {
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
                                toastr['warning']('<h5>Các trạm sau chưa cập nhật - Do chưa đặt yêu cầu phải có tối thiểu 02 nhóm thông số, trong đó có nhóm II. Mỗi nhóm thông số, có tối thiểu 01 thông số sử dụng để tính VN_WQI: </h5>' + station_names);
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

