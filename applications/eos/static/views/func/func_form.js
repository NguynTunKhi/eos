
var reference;

$(document).ready(function() {
    $('#jstree').jstree({ 
        'core' : {
            'check_callback' : true,
            'data' : {
                'url' : 'call/json/func_json',
                'data' : function (node) {
                    return { 'id' : node.id };
                }
            },
        },
        "themes" : { "stripes" : false },
        'contextmenu' : {'items' : customMenu},
        'plugins' : [ 'contextmenu', 'sort', 'wholerow' , 'crrm', 'themes']
    }).bind(
        'select_node.jstree', function(evt, data){
            node_clicked();
        }
    ).bind(
        'rename_node.jstree', function(e, data){
            var ref = $('#jstree').jstree(true);
            var sel = ref.get_selected();
            
            if(!sel.length) { return false; }

            var vars = {'id' : parseInt(sel[0]),
                        'name' : ref.get_text(sel[0]),
                        'old_name': data.node.original.text
                       };
            var url = $('#rename-url').val() + "?" + $.param(vars);
            app.showProgress();
            $.ajax({
                "type": "POST",
                "url": url,
                "data": [],
                "success": function(data) {
                    eval(data);
                    app.hideProgress();
                }
            });
        }
    );
    
    reference = $('#jstree').jstree(true);
        
    $("#btnAdd").click(function(){
        $(this).closest('form').submit();
    });
    app.showProgress();
    $.ajax({
        "type": "POST",
        "url": $('#get-func-url').val(),
        "data": [],
        "success": function(data) {
            eval(data);
            app.hideProgress();
        }
    });
    
    if ($('#parent-id').val() != 'None') {
        func_parent_id = $('#parent-id').val();
    } else {
        func_parent_id = 1;
    }
    
    $("#func_parent_id").val(func_parent_id);
});

function customMenu(node) {
    // The default set of all items
    var items = {
        renameItem: { // The "rename" menu item
            label: $('#label-rename').val(),
            action: function (obj) {
                var temp = $('#jstree').jstree('edit', node.id);
            }
        },
        deleteItem: { // The "delete" menu item
            label: $('#label-del').val(),
            action: function () {
                var ref = $('#jstree').jstree(true);
                ref.delete_node(node.id);
                
                var vars = {id : node.id};
                var url = $('#del-url').val() + "?" + $.param(vars);
                app.showProgress();
                $.ajax({
                    "type": "POST",
                    "url": url,
                    "data": [],
                    "success": function(data) {
                        eval(data);
                        app.hideProgress();
                    }
                });
            },
            _disabled : $('#jstree').jstree('is_parent', node) | node.id == 1
        }
    };

    return items;
}

function node_clicked() {
    var sel = $('#jstree').jstree('get_selected');
    $("#func_parent_id").val(sel[0]);
}

function setCode() {
    $("#func_code").val("...|" + $("#func_name").val());
    return;
}

function confirmBack() {
    window.history.back();
}