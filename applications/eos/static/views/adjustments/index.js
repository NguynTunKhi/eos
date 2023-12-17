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
    var aoColumns = [
        {'sWidth' : '3%', 'bSortable' : false},
        {'sWidth' : '30%'},
        {'sWidth' : '14%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'},
        {'sWidth' : '7%'},
        {'sWidth' : '5%'},
        {'sWidth' : '10%'},   // For check box column
        {'sWidth' : '3%'},   
    ];

    var aoClass = ['', 'text-left', 'text-left', 'text-left','' , '', '', '', ''];
    loadDataTable({

        aoColumns: aoColumns,
        aoClass: aoClass,
        
    });
    
    return true;
}

function reloadDatatable_Adjustment() {
    // oTable[0].fnFilter('');
    location.reload();
    $( ".btnAlert" ).trigger( "click" );
}