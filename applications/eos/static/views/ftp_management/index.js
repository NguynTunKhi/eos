$(document).ready(function() {
    loadDataTableForPage();

    $('#btn_search').click(function(){
        loadDataTableForPage();
    });
});

function reloadDatatable_Ftp_management() {
    oTable[0].fnFilter('');
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '3%'}, // idx
        {'sWidth' : '32%'}, // ftpIP
        {'sWidth' : '10%'}, // ftpPort
        {'sWidth' : '10%'}, // ftpUser
        {'sWidth' : '10%'}, // user created
        {'sWidth' : '10%'}, // created at
        {'sWidth' : '10%'}, // updated at
        {'sWidth' : '10%'}, // administration level
        {'sWidth' : '5%'} // check box
    ];

    var aoClass = ['', 'text-left', '', '', '', '', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
            aoData.push({
                "name": "administration_level", "value": $('#administration_level').val()
            });
        },
    });

    return true;
}

