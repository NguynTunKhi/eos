$(document).ready(function() {
    validator = $("form#form_groups").validate({
        rules: {
            role: 'required',
        },
        messages: {
        }
    }); 
    $('#btnSave').click(function() {
        if (!validateForm()) return;
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function() {
                $('#form_groups').submit();
            }
        });
    });
    $('#btn-delete').click(function() {
        var arr = $("#home2").find(".select_item");
        var par;
        var url;
        var role_id = $('#btnSave').attr('data-id');
        var arrayData = role_id;
        for(var i = 0; i < arr.length; i++) {
            var item = $(arr[i]);
            if(item.is(':checked')) {
                arrayData += ',' + item.val();
            }
        }
        par = {
            'arrayData': arrayData
        };
        url = $('#del-action').val() + "?" + $.param(par);
        $.ajax({
            dataType: 'json',
            url: url,
            success: function(data){
                if(data.success){
                    oTable[0].fnDraw();
                    oTable[1].fnDraw();
                    $("input[type='checkbox']").prop('checked', false);
                }
            }
        });
    });
    
    $('#btn-add').click(function() {
        var arr = $("#profile2").find(".select_item");
        var par;
        var url;
        var role_id = $(this).attr('data-id');
        var arrayData = role_id;
        for(var i = 0; i < arr.length; i++) {
            var item = $(arr[i]);
            if(item.is(':checked')) {
                arrayData += ',' + item.val();
            }
        }
        par = {
            'arrayData': arrayData
        };
        url = $('#add-action').val() + "?" + $.param(par);
        $.ajax({
            dataType: 'json',
            url: url,
            success: function(data){
                if(data.success){
                    oTable[0].fnDraw();
                    oTable[1].fnDraw();
                    $("input[type='checkbox']").prop('checked', false);
                }
            }
        });
    });

    // $('#btn-delete').removeClass('hide');
    // $('#btn-add').addClass('hide');
    // $('#btn-delete').removeClass('disabled');
    // $('#btn-add').addClass('disabled');
    // $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
        // var currentTab = $(e.target).text(); // get current tab
        // var LastTab = $(e.relatedTarget).text(); // get last tab
        // if (currentTab == ' Users not in group'){
            // // $('#btn-delete').addClass('hide');
            // // $('#btn-add').removeClass('hide');
            // $('#btn-delete').addClass('disabled');
            // $('#btn-add').removeClass('disabled');
        // } else {
            // // $('#btn-delete').removeClass('hide');
            // // $('#btn-add').addClass('hide');
            // $('#btn-delete').removeClass('disabled');
            // $('#btn-add').addClass('disabled');
        // }
    // });
});

function validateForm() {
    return true;
}
function loadDataTableForPage() {
    var sDom = "<'top' <'col-sm-1 drop-down-list' l><'col-sm-6' f><'col-sm-5 alignRight' i>><'clear'><'middle't><'clear'><'bottom' <'col-sm-6 go-to-page'> <'col-sm-6 alignRight' p>><'clear'>";
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [  
                        { "sWidth": "5%", "bSortable": false },
                        { "sWidth": "30%" },
                        { "sWidth": "30%" },
                        { "sWidth": "30%" },
                        { "sWidth": "5%" }
                    ];
    var aoClass = ['', 'text-left', 'text-left', 'text-left', ''];
    
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom
    });
}

function loadDataTableForPage_1() {
    var sDom = "<'top' <'col-sm-1 drop-down-list' l><'col-sm-6' f><'col-sm-5 alignRight' i>><'clear'><'middle't><'clear'><'bottom' <'col-sm-6 go-to-page'> <'col-sm-6 alignRight' p>><'clear'>";
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [  
                        { "sWidth": "5%", "bSortable": false },
                        { "sWidth": "30%" },
                        { "sWidth": "30%" },
                        { "sWidth": "30%" },
                        { "sWidth": "5%" }
                    ];
    var aoClass = ['', 'text-left', 'text-left', 'text-left', ''];
    
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        iTable: 1
    });
}

function ValidateForm() {
    if (!validateMandatoryForm()) return false;
    if (!validateTypeForm()) return false;
    if (!validateBussinessForm()) return false;
    if (!validateLengthForm()) return false;
    return true;
}

function validateMandatoryForm() {
    if(!validator.form()) return false;
    return true;
}

function validateTypeForm() {
    return true;
}

function validateBussinessForm() {
    return true;
}

function validateLengthForm() {
    if ($('#auth_group_role').val().trim().length > 256){
        app.showError(app.translate("Please input group name with max 256 characters!"))
        return false;
    }
    if ($('#auth_group_description').val().trim().length > 1024){
        app.showError(app.translate("Please input description with max 1024 characters!"))
        return false;
    }
    return true;
}