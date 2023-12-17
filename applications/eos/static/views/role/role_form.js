

$(document).ready(function() {
    validator = $("form#frmMain").validate({
    rules: {
        qcvn_name: 'required',
        qcvn_code: 'required',
        qcvn_type: 'required',
    },
    messages: {
    }
    });
    $('#btnSave').click(function() {
        if (!ValidateForm()) return;
        $('#form_role').submit();
    });
    
    $('#btn-delete').click(function() {
        var arr = $('.select_item_0');
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
        var arr = $('.select_item_1');
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
    
    $('#btn-add').addClass('hide');
    $('#btn-delete').removeClass('hide');
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var target = $(e.target).attr("href"); // activated tab
        if (target == '#profile2') {
            $('#btn-add').removeClass('hide');
            $('#btn-delete').addClass('hide');
        } else {
            $('#btn-add').addClass('hide');
            $('#btn-delete').removeClass('hide');
        }
    });
});

function loadDataTableForPage() {
    if (typeof loadDataTable == "function"){
        var sDom = "<'top' <'col-sm-1 drop-down-list' l><'col-sm-6' f><'col-sm-5 alignRight' i>><'clear'><'middle't><'clear'><'bottom' <'col-sm-6 go-to-page'> <'col-sm-6 alignRight' p>><'clear'>";
        var sAjaxSource = $("#custom_datatable_0").attr("data-url") + "?" + $.param({role_id: $('#btnSave').attr('data-id')});
        var aoColumns = [  
                            { "sWidth": "5%", "bSortable": false },
                            { "sWidth": "35%" },
                            { "sWidth": "60%" }
                        ];
        var aoClass = ['', 'text-left', 'text-left'];
        
        loadDataTable({
            sAjaxSource: sAjaxSource,
            aoColumns: aoColumns,
            aoClass: aoClass,
            sDom: sDom
        });
    } else {
        setTimeout(loadDataTableForPage, 30);
    }
}
function loadDataTableForPage_1() {
    if (typeof loadDataTable == "function"){
        var sDom = "<'top' <'col-sm-1 drop-down-list' l><'col-sm-6' f><'col-sm-5 alignRight' i>><'clear'><'middle't><'clear'><'bottom' <'col-sm-6 go-to-page'> <'col-sm-6 alignRight' p>><'clear'>";
        var sAjaxSource = $("#custom_datatable_1").attr("data-url") + "?" + $.param({role_id: $('#btnSave').attr('data-id')});
        var aoColumns = [  
                            { "sWidth": "5%", "bSortable": false },
                            { "sWidth": "35%" },
                            { "sWidth": "60%" }
                        ];
        var aoClass = ['', 'text-left', 'text-left'];
        
        loadDataTable({
            sAjaxSource: sAjaxSource,
            aoColumns: aoColumns,
            aoClass: aoClass,
            sDom: sDom,
            iTable: 1
        });
    } else {
        setTimeout(loadDataTableForPage_1, 30);
    }
}

function ValidateForm() {
    if (!validateMandatoryForm()) return false;
    if (!validateTypeForm()) return false;
    if (!validateBussinessForm()) return false;
    if (!validateLengthForm()) return false;
    return true;
}

function validateMandatoryForm() {
    if ($('#role_name').val().trim() == ''){
        $.message({s_content: $('#msg-not-empty').val(),
            s_img: 'error',
            b_cancel: false,
            fn_call: function(){
                $('#role_name').focus();
            }
        });
        return false;
    }
    return true;
}

function validateTypeForm() {
    return true;
}

function validateBussinessForm() {
    return true;
}

function validateLengthForm() {
    if ($('#role_name').val().trim().length > 256){
        $.message({s_content: $('#msg-max-length').val(),
            s_img: 'error',
            b_cancel: false,
            fn_call: function(){
                $('#role_name').focus();
            }
        });
        return false;
    }
    if ($('#role_description').val().trim().length > 1024){
        $.message({s_content: $('#msg-max-length-1024').val(),
            s_img: 'error',
            b_cancel: false,
            fn_call: function(){
                $('#role_description').focus();
            }
        });
        return false;
    }
    return true;
}