$(document).ready(function() {
    loadDataTableForPage();
    $('#btn_search').click(function(){
        oTable[0].fnFilter('');
    });
});

function handleDelete(e){
    var url = 'call/json/delete_indicator'
    var id = e.id
    app.showConfirmBox({
        content: app.translate('sure_to_delete'),
        callback: function() {
            deleteMeasuring(id, url);
        }
    });
}

function deleteMeasuring(id, url){
       app.postAjax({
        url: url,
        data: {id},
        callback: function(res){
            if(res.success){
                 if(res.data) {
                    app.showError(app.translate('alert_cant_delete'))
                 } else {
                    app.showNotification({"content":app.translate('alert_delete_success')})
                    loadDataTableForPage();
                 }}
            }
    });
}

function alert(text, type){
    toastr.options.positionClass = "toast-top-center";
    toastr.options.timeOut=1500;
    toastr[type](text);
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var length_column = $('#tr-table>th').length;
    console.log('tesss length->>', length_column);

    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '20%'},
        {'sWidth' : '20%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},
        {'sWidth' : '5%'},
        // {'sWidth' : '15%'},
        // {'sWidth' : '15%'},
         //{'sWidth' : '5%'},   // For check box column
    ];
    if(length_column<6){
       aoColumns = [{'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '20%'},
        {'sWidth' : '20%'},
        {'sWidth' : '10%'},
        {'sWidth' : '5%'},
       ]
    }

    var aoClass = ['', 'text-left', 'text-left', '', '', 'text-center', 'text-right', ''];
    // var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        // sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "type", "value": $('#type').val()
            });
            aoData.push({
                "name": "sometext", "value": $('#sometext').val()
            });
        },
    });
    
    return true;
}