var isLoadDatatable = false;
var $th = $('.tableFixHead').find('thead th')
$('.tableFixHead').on('scroll', function() {
  $th.css('transform', 'translateY('+ this.scrollTop +'px)');
});
$(document).ready(function () {
    $('#month_date').datetimepicker({
        timepicker: false,
        // format: "Y-M",
        // viewMode: "months",
        // minViewMode: "months"
    });
    $('#cbbAddedColumns_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')

    $('#btnExportExcel').on('click', function (e) {
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

    $('body').on('click', '.btnCustomSearch', function (e) {
        time = new Date();
        date = new Date().toISOString().split("T")[0];
        if (!$('#cbbStationId').val()) {
            e.preventDefault();
            app.showError(app.translate('Please select a station first!'));
            return false;
        }
        if (!$('#Month').val()) {
            e.preventDefault();
            app.showError(app.translate('Please select month!'));
            return false;
        }
        if (!$('#Year').val()) {
            e.preventDefault();
            app.showError(app.translate('Please select year!'));
            return false;
        }
        $('#btnExportExcel').removeClass('hide');
        oTable[0].fnFilter();
        if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
    });

    $('#cbbStationType, #cbbProvinceId').change(function () {
        var url = $(this).data('url');
        var data = {};
        app.postAjax({
            url: url,
            data: {filter_value: $('#cbbStationType').val().trim() + ';' + $('#cbbProvinceId').val().trim()},

            callback: function (res) {
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

        if ($('#cbbStationId').val() == '') $('#btnExportExcel').addClass('hide');
    });
    if ($('#cbbStationType').val()) {
        $('#cbbStationType').trigger('change');
    }
    if ($('#cbbProvinceId').val()) {
        $('#cbbProvinceId').trigger('change');
    }
    if ($('#cbbStationId').val()) {
        isLoadDatatable = true;
        $('#cbbStationId').trigger('change');
    } else {
        loadDataTableForPage();
    }
});
function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth': '5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '3.5%'},
        {'sWidth': '11%'},
    ];

    var aoClass = ['','','','','','','','','','','','','','','','','','','','','','','','','',''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
}