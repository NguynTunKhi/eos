$(document).ready(function() {
    // Load nestable
    var url = $('#agentsTree').data('url');
    var html = $('#agentsTree').load(url);
    showHideButtonSelectStation();
    
    var updateOutput = function (e) {
         var list = e.length ? e : $(e.target),
                 output = list.data('output');
         if (window.JSON) {
             output.val(window.JSON.stringify(list.nestable('serialize')));//, null, 2));
         } else {
             output.val('JSON browser support required for this demo.');
         }
     };
     
    $('#agentsTree').nestable({
         group: 1
     }).on('change', updateOutput);

    loadDataTableForPage();

    $('body').on('click', '#btnSearchForAgent', function(e){
        var keyword = $('#txtSearchForAgent').val();
        
        // Todo : search tree here
        
    });

    $('body').off('click', '.dd-handle');
    $('body').on('click', '.dd-handle', function(e){
        var id = '';
        if ($(this).hasClass('active')){
            $(this).removeClass('active');
            // Todo: update datatable
        }
        else {
            $('.dd-handle').removeClass('active');
            $(this).addClass('active');
            id = $(this).data('id');
        }
        $('#hfAgentId').val(id);
        showHideButtonSelectStation();
        // Reload datatable
        oTable[0].fnFilter('');
    });
    
    
});

function showHideButtonSelectStation() {
    var id = $('#hfAgentId').val();
    if (id){
        $('#btnSelectStationFromPopup').removeAttr('disabled');
    } else {
        $('#btnSelectStationFromPopup').attr('disabled', 'disabled');
    }
}

function loadDataTableForPage() {
    var sAjaxSource = $("#custom_datatable_0").attr("data-url");
    var aoColumns = [
        {'sWidth' : '10%', 'bSortable' : false},
        {'sWidth' : '50%'},
        {'sWidth' : '30%'},
        {'sWidth' : '10%'},
    ];

    var aoClass = ['', 'text-left', 'text-left', ''];
    var sDom = "<'middle't><'clear'>";
    loadDataTable({
        sAjaxSource: sAjaxSource,
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "agent_id", "value": $('#hfAgentId').val()
            });
        },
        iTable:0
    });

    return true;
}

function addStationToAgent() {
    var agentId = $('#hfAgentId').val();
    var stationId = $('#hfStationId').val();
    var stationType = $('#hfStationType').val();
    var url = $('#hfUrlLinkAgentToStation').val();
    app.postAjax({
        url: url,
        data: {agentId: agentId, stationId: stationId, stationType: stationType},
        callback: function (res) {
            if (res.success) {
                oTable[0].fnDraw();
            } else {
                app.showError(res.message);
            }
        }
    });
}