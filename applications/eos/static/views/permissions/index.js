
$(document).ready(function() {
    loadDataTableForPage();
    
    $("#btnSave").click(function(){
        getCheckboxData('#btnSave', "#custom_datatable_0 tbody tr");
    });
    
    $("#btnSaveTable").click(function(){
        getCheckboxData('#btnSaveTable', "#custom_datatable_1 tbody tr");
    });
    
    // chinh CSS cua table list station
    var wrap = $('#custom_datatable_0').closest('.middle');
    wrap.removeClass('row');
    // chinh CSS cua table list station
    wrap = $('#custom_datatable_1').closest('.middle');
    wrap.removeClass('row');
});

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        { "sWidth": "5%", },
        { "sWidth": "25%" },
        { "sWidth": "70%" },
    ];

    var aoClass = ['', 'text-left', 'text-left'];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        // sDom: "<'row top' <'col-sm-6' f><'col-sm-6 text-right' i>><'clear'><'row middle't><'clear'><'row bottom' ><'clear'>",
        sDom: 'ft',
        customInfo: {dblclickOnRow: false},
        responsive: true,
                
    });
}

function getCheckboxData(btn, dom) {
    /* Get checkboxes value to 'data', format :
     * controller_name,permission_name,...; (6 permission)
     * controller_name,permission_name,...; (6 permission)
     * (if no permission blank value is left)
     */
    var rows = $(dom);
    var data_chk = '';
    var total = rows.length;
    for (var i = 0; i < total; i++){
        var temp = '';
        var chks = $(rows[i]).find("input[type=checkbox]");
        var t1 = chks.length;
        for (var j = 0; j < t1; j++){
            var chk = $(chks[j]);
            if(temp == ''){
                temp += chk.attr("name");
            }
            if (chk.prop("checked")){
                temp += ",";
                temp += chk.val();
            }
        }
        if (data_chk !== ""){
            data_chk += ";";
        }
        data_chk += temp;
    }
    
    // Parameters pass to server
    var group_id = $(btn).attr('data-group');
    var msg = $(btn).attr('data-confirm');
    if (btn == '#btnSave') {
        var type = 'controller';
    } else if (btn == '#btnSaveTable') {
        var type = 'table';
    } else {
        var type = '';
    }
    
    app.showConfirmBox({
        content: msg,
        callback: function () {
            // Call ajax to update permissions
            app.postAjax({
                url: $(btn).attr('data-url'),
                data: $.param({'permissions' : data_chk, 'group_id' : group_id, 'type' : type}),
                callback: function (data) {
                    if (data.success){
                        toastr.options.timeOut = "5000";
                        toastr['success'](app.translate('JS_MSG_SAVE_SUCCESS'));
                    } else {
                        app.showError(data.message)
                    }
                }
            });
        }
    });
}
