var isLoadDatatable = false;

$(document).ready(function () {
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
        if (!$('#cbbProvinceId').val() && !$('#cbbArea').val())
        {
            e.preventDefault();
            app.showError(app.translate('Please select a province!'));
            return false;
        }

        $('#btnExportExcel').removeClass('hide');
        oTable[0].fnFilter();
        if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
    });
    $('#cbbArea').change(function () {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {area: $('#cbbArea').val()},
            callback: function (res) {
                if (res.success) {
                    $('#cbbProvinceId').html(res.html);
                    $('#cbbProvinceId').trigger("chosen:updated");
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

    if ($('#cbbProvinceId').val()) {
        $('#cbbProvinceId').trigger('change');
    }
    else {
        loadDataTableForPage();
    }
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth': '3%'},
        {'sWidth': '20%'},
        {'sWidth': '20%'},
        {'sWidth': '20%'},
    ];

    var aoClass = ['', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
    return true;
}