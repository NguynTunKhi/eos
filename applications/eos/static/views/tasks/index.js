/**
 * Created by Admin on 8/1/2017.
 */

$(document).ready(function() {
    loadDataTableForPage();
    loadDataTableForPage_worker();
    setTimeout(function(){AutoReload();}, 10000);
    setTimeout(function(){AutoReload_1();}, 10000);
    
    $('#btnTaskGetData').click(function() {
        var thisInstance = this;
        app.showConfirmBox({
            content: app.translate('MSG_CONFIRM_RUN_TASK'),
            callback: function () {
                var url = $(thisInstance).attr("data-url");
                var data = "";
                $.ajax({
                    type: "POST",
                    url: url,
                    data: data,
                    dataType: 'json',
                    success: function(){
                        $('#btnTaskGetData').addClass('disabled');
                        $('#custom_datatable_0').DataTable().ajax.reload(null, false);
                    },
                    error: function(err){
                        app.showError(err.status + ": " + err.statusText);
                    }
                });
            }
        });
        
    });
});

function AutoReload() {
    $('#custom_datatable_0').DataTable().ajax.reload(null, false);
    setTimeout(function(){AutoReload();}, 10000);
}

function AutoReload_1() {
    $('#custom_datatable_1').DataTable().ajax.reload(null, false);
    setTimeout(function(){AutoReload_1();}, 10000);
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '40%'},
        {'sWidth' : '15%'},
        {'sWidth' : '10%'},
        {'sWidth' : '15%'},
        {'sWidth' : '15%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', '', '',''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        fnCustomCallback: function(data){
            $('#alive-task').html(data.alive_task);
            // Enable / Disable start scheduler daily task button
            if (data.alive_task > 0){
                $('#btnTaskGetData').addClass('disabled');
            }
        }
    });
}

function loadDataTableForPage_worker() {
    var sAjaxSource = $("#custom_datatable_1").attr("data-url");
    var aoColumns = [
        {'sWidth' : '5%', 'bSortable' : false},
        {'sWidth' : '24%'},
        {'sWidth' : '15%'},
        {'sWidth' : '18%'},
        {'sWidth' : '18%'},
        {'sWidth' : '10%'},
        {'sWidth' : '10%'}
    ];

    var aoClass = ['', 'text-left', 'text-left', '', '','', ''];
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable: 1,
        sDom: "<'top' <'col-sm-6 ' i> <'col-sm-6 '>><'clear'><'middle't><'clear'><'bottom'  ><'clear'>",
        fnCustomCallback: function(data){
            $('#active-worker').html(data.active_worker);
        }
    });
}