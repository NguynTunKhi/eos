$(document).ready(function() {
    loadDataTableForPage();
    // var loadtable = false;
    // var search = false;

    // $('#btn_search').click(function(){
        // if (loadtable == false) {
            // loadtable = loadDataTableForPage();
        // }
        // if (search == true) {
            // oTable[0].fnFilter('');
        // }
        // search = true;
    // });
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
    $('#province_id').change(function(){
        $("#btn_search").click()
    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '30%'},
        {'sWidth' : '50%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},   // For check box column
    ];

    var aoClass = ['', '', 'text-left', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#province_id').val()
            });
        },
    });
    
    return true;
}