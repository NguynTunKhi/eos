$(document).ready(function() {
    loadDataTableForPage();
    loadDataTableForPage_1();

    $('body').on('click', '#btnSearchForArea', function(e){
        var keyword = $('#txtSearchForArea').val();
        oTable[0].fnFilter(keyword);
    });

    $('body').on('click', '#custom_datatable_0 tbody tr' , function(e){
        if ($(this).hasClass('selected')){
            $('#hfAreaId').val('');
            $(this).removeClass('selected');
        } else {
            $(this).closest('tbody').find('tr').removeClass('selected');
            $(this).addClass('selected');
            var id = $(this).data('id');
            $('#hfAreaId').val(id);
        }
        oTable[1].fnDraw();
        showHideButtonSelectStation();
    });
});

function showHideButtonSelectStation() {
    var id = $('#hfAreaId').val();
    if (id){
        $('#btnSelectStationFromPopup').removeAttr('disabled');
        $('#btnRemoveLinkStationFromArea').removeAttr('disabled');
    } else {
        $('#btnSelectStationFromPopup').attr('disabled', 'disabled');
        $('#btnRemoveLinkStationFromArea').attr('disabled', 'disabled');
    }
}

function reloadDatatable() {
    oTable[0].fnDraw();
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '25%'},
        {'sWidth' : '50%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},
        {'sWidth' : '5%'}
    ];

    var aoClass = ['', 'text-left', 'text-left', ''];
    var sDom = "<'middle't><'clear'><'row bottom' <'col-sm-6 text-left' li><'col-sm-6 text-right' p>><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomDrawCallback: function () {
            $('#hfAreaId').val('');
            showHideButtonSelectStation();
        }
    });
    
    return true;
}

function loadDataTableForPage_1() {
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [
        {'sWidth' : '10%', 'bSortable' : false},
        {'sWidth' : '35%'},
        {'sWidth' : '35%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', ''];
    var sDom = "<'middle't><'clear'><'row bottom' <'col-sm-6 text-left' li><'col-sm-6 text-right' p>><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "area_id", "value": $('#hfAreaId').val()
            });
        },
        iTable:1
    });

    return true;
}

function addStationToArea() {
    var areaId = $('#hfAreaId').val();
    var stationId = $('#hfStationId').val();
    var stationType = $('#hfStationType').val();
    var url = $('#hfUrlLinkAreaToStation').val();
    app.postAjax({
        url: url,
        data: {areaId: areaId, stationId: stationId, stationType: stationType},
        callback: function (res) {
            if (res.success) {
                oTable[1].fnDraw();
            } else {
                app.showError(res.message);
            }
        }
    });
}