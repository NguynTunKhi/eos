/**
 * Created by Admin on 8/2/2017.
 */

$(document).ready(function() {
    
    loadDataTableForPage_1();

    $('.scroll_content_adjust_data').slimscroll({
        height: '380px'
    });
    
    $("form#frmPopupAdjust").validate({
        rules: {
            adjust_value: {
                required: true,
                number: true,
            },
        },
        messages: {
            adjust_value: app.translate('Input digits value!'),
        },
    });

    $('body').off('click', '.modal .btnSave2');
    $('body').on('click', '.modal .btnSave2', function (e) {
        var currentForm = $("form#frmPopupAdjust");
        if(currentForm.validate().form() == false){
            return;
        }
        if(!validateBussinessForPopupAdjust()){
            return false;
        }
        app.showConfirmBox({
            content: app.translate('JS_MSG_CONFIRM_SAVE'),
            callback: function () {
                var url = currentForm.attr('action');
                $.ajax({
                    type: "POST",
                    dataType: 'json',
                    url: url,
                    data: currentForm.serialize(),
                    success: function(data){
                        if(data.success){
                            currentForm.closest('.ModalWrap').remove();
                            eval($(".graph_detail_adjust_data").first().data("callback"));
                        } else {
                            currentForm.closest('.ModalWrap').find(".errors").html(data.message);
                        }
                    },
                    error: function(err){
                        instance.find(".errors").html(err.status + ": " + err.statusText);
                    }
                 });
            }
        });
    });

    $(".ModalWrap > .modal > .modal-content").draggable({
        handle: ".modal-header"
    });
});

function validateBussinessForPopupAdjust() {
    return true;
}

function loadDataTableForPage_1() {
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [
        {'sWidth' : '4%'},
        {'sWidth' : '16%'},
        {'sWidth' : '16%'},
        {'sWidth' : '16%'},
        {'sWidth' : '16%'},
        {'sWidth' : '16%'},
        {'sWidth' : '16%'},
    ];

    var aoClass = ['', '', '', ];
    var sDom = "<'middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable: 1,
        sDom: sDom,
    });
    
    return true;
}