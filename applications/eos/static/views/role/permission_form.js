
$(function() {
    $('#jstree').jstree({ 
        'core': {
            'data': {
                'url': $('#jstree-url').val(),
                'data': function (node) {
                    return { 'id': node.id };
                }
            },
        },
        'contextmenu': { 'items': customMenu, 'select_node': false },
        'checkbox': { "keep_selected_style": false },
        'plugins' : [ 'contextmenu', 'checkbox', 'sort', 'wholerow' ]
    });
});

function customMenu(node) {
    var items = { 
        getFuncCode: { 
            label: $('#lbl-get-func-code').val(),
            action: function() {
                var url = $('#func-code-url').val() + "?" + $.param({ func_id: node.id });
                ajax(url, [], ':eval');
            }
        }
    };
    return items;
}


function update_permission() {
    var selected_nodes = ($('#jstree').jstree('get_selected')).toString();
    var vars = { role_id: $('#record-id').val(), selected_nodes: selected_nodes }
    var url = $('#update-url').val() + '?' + $.param(vars);
    window.location = url;
}