$(document).ready(function() {
    loadDataTableForPage();
//    ajax_get_list();

});

function ajax_get_list(){
    var url = $("#ajax_tb_0").attr("data-url");
    $.ajax({
      type: "POST",
      url: url,
      data: {},
      success: function(rs) {
        $.each(rs['aaData'], function( index, value ) {
            var html = '<td>'+ value[0] +'</td>' + '<td>'+ value[1] +'</td>' + '<td>'+ value[2] +'</td>' + '<td>'+ value[3] +'</td>';
             $('#ajax_tb_0 > tbody').append('<tr>' + html + '</tr>')
        });
      }
    });
}

function reloadDatatable() {
    oTable[0].fnDraw();
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '35%'},
        {'sWidth' : '10%'},
        {'sWidth' : '55%'},
    ];

    var aoClass = ['', 'text-left', '', 'text-left'];
//    var sDom = "<'middle't><'clear'><'row bottom' <'col-sm-6 text-left' li><'col-sm-6 text-right' p>><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
//        sDom: sDom,
        fnCustomDrawCallback: function () {
            oTable[0].fnDraw();
        }
    });

    return true;
}



