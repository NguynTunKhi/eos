$(document).ready(function() {
    loadDataTableForPage();
    loadDataTableForPage_1();

    $('body').on('click', '#btnSearchForArea', function(e){
        var keyword = $('#txtSearchForArea').val();
        oTable[0].fnFilter(keyword);
    });

    $('body').on('click', '.btnCustomSearch', function (e) {
        oTable[1].fnFilter('');
    });


});


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
        }
    });

    return true;
}

function loadDataTableForPage_1() {
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '41%'},
        {'sWidth' : '51%'},
        {'sWidth' : '3%'},   // For check box column
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
                "name": "type", "value": $('#type').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#txtSearchForStation').val()
            });

        },
        iTable:1
    });

    return true;
}
