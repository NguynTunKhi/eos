$(document).ready(function() {
    loadDataTableForPage();

    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%', 'bSortable' : false},
        {'sWidth' : '9%'},
        {'sWidth' : '15%'},
        {'sWidth' : '5%'},
        {'sWidth' : '12%'},
//        {'sWidth' : '12%'},
//        {'sWidth' : '12%'},
//        {'sWidth' : '10%'},
        {'sWidth' : '18%'},
        {'sWidth' : '3%'},   // For check box column
    ];

    var aoClass = ['', 'text-left', 'text-left','', '', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            // aoData.push({
            //     "name": "type", "value": $('#type').val()
            // });
        },

    });

    return true;
}
