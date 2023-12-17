var isLoadDatatable = true;
var $th = $('.tableFixHead').find('thead th')
$('.tableFixHead').on('scroll', function () {
    $th.css('transform', 'translateY(' + this.scrollTop + 'px)');
});
$(document).ready(function () {
    $('#cbbAddedColumns_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
    loadDataTableForPage();
    $('body').on('click', '.btnCustomSearch', function (e) {
         if (!validateTime()) {
            e.preventDefault();
            return false;
        }
        oTable[0].fnFilter();
        if (typeof oTable[1] !== 'undefined') oTable[1].fnFilter();
    });

    $('#btnExportExcel').on('click', function (e) {
        var url = $(this).attr("data-url");
        window.open(url);
    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth': '40%'},
        {'sWidth': '5%'},
        {'sWidth': '5%'},
        {'sWidth': '5%'},
    ];

    var aoClass = ['', 'text-left'];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
    });
    return true;
}

function validateTime() {
    var dt0_from_date = $('#dt0_from_date');
    var dt0_to_date = $('#dt0_to_date');
    if (dt0_from_date.val() == '') {
        app.showError(app.translate('ERR_Day_Input_Blank'));
        return false;
    }
    var fromDate = new Date(dt0_from_date.val());
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime(maxDate.getTime() + myTimeZone * 60 * 60 * 1000);
    var minDate = new Date(dt0_to_date.val());
    if (dt0_to_date.val() == '') {
        toDate = new Date();
        var tempDate = toDate.toISOString().split("T")[0];
        $('#dt0_to_date').val(tempDate);
        minDate = new Date();
    }
    //minDate.setDate(minDate.getDate() - 365);
    if (toDate > maxDate) {
        app.showError(app.translate('ERR_Day_Input_To_Date_Max_Exceed'));
        return false;
    }
    if (fromDate > toDate) {
        app.showError(app.translate('ERR_Day_Search'));
        return false;
        // $('#dt0_to_date').val('');
    }
//        if (fromDate < minDate) {
//            app.showError(app.translate('ERR_Day_Input_From_Date_1_YEAR'));
//            return false;
//        }
    return true;
}