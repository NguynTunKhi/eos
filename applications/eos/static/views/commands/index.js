$(document).ready(function() {
    loadDataTableForPage();
        
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
    
    $('.btnAlert').click(function(){
        swal({
            title: "Command sent!",
            type: "success",
            // confirmButtonColor: "#DD6B55",
            // confirmButtonText: "Yes, delete it!",
        });
    });
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%'},
        {'sWidth' : '15%'},
        {'sWidth' : '12%'},
        {'sWidth' : '25%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},
        {'sWidth' : '5%'},
        {'sWidth' : '5%'},
//        {'sWidth' : '5%'},
    ];

    var aoClass = ['', 'text-left', '', 'text-left', '', '', '', '', '', ''];
    // var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        // sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "station_id", "value": $('#station_id').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "station_type", "value": $('#station_type').val()
            });
        },
    });
    
    return true;
}

function reloadDatatable_Command() {
    // oTable[0].fnFilter('');
    
    $( ".btnAlert" ).trigger( "click" );
}