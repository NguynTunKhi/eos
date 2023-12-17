
$(document).ready(function() {
    loadDataTableForPage_online();
    loadDataTableForPage_inactive();
    
    // Block 2
    $('.progress .progress-bar').css("width",
        function() {
            return $(this).attr("aria-valuenow") + "%";
        }
    );

    $('.scroll_scs1, .scroll_scs2').slimscroll({
        height: '450px'
    });
    
    $('body').on('click', '#btn_scs1_search', function (e) {
       oTable['scs1'].fnFilter(); 
    });
    
    $('body').on('click', '#btn_scs2_search', function (e) {
       oTable['scs2'].fnFilter(); 
    });
    
    $('body').on('change', '#scs1_status', function (e) {
       oTable['scs1'].fnFilter(); 
    });
    
    $('body').on('change', '#scs2_condition', function (e) {
       oTable['scs2'].fnFilter(); 
    });
});

function loadDataTableForPage_online() {
    var aoColumns = [
        {'sWidth' : '10%'},
        {'sWidth' : '45%'},
        {'sWidth' : '45%'},
    ];

    var aoClass = ['', 'text-left','text-left'];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable: 'scs1',
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "area_id", "value": $('#global_area_id').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#global_province_id').val()
            });
        },
    });
    
    // chinh CSS cua table list station
    var wrap = $('#custom_datatable_scs1').closest('.middle');
    wrap.removeClass('row');
    return true;
}

function loadDataTableForPage_inactive() {
    var aoColumns = [
        {'sWidth' : '10%'},
        {'sWidth' : '60%'},
        {'sWidth' : '30%'},
    ];

    var aoClass = ['text-left', ''];
    var sDom = "<'row middle't><'clear'>";
    loadDataTable({
        aoColumns: aoColumns,
        aoClass: aoClass,
        iTable: 'scs2',
        sDom: sDom,
        fnCustomServerData: function (sSource, aoData, fnCallback) {
            aoData.push({
                "name": "area_id", "value": $('#global_area_id').val()
            });
            aoData.push({
                "name": "province_id", "value": $('#global_province_id').val()
            });
        },
    });
    
    // chinh CSS cua table list station
    var wrap = $('#custom_datatable_scs2').closest('.middle');
    wrap.removeClass('row');
    return true;
}