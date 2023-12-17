$(document).ready(function() {
    loadDataTableForPage();

    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});



function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '85%'},
        {'sWidth' : '5%'},
        {'sWidth' : '5%'},


    ];

//    var aoClass = ['', 'text-left', '', '', '', 'text-right', 'text-right', ''];
    // var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
//        aoClass: aoClass,
        // sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
        },
    });

    return true;
}