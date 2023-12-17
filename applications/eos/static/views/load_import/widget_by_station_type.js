
var wbstInterval = setInterval(function () {
    if (typeof jQuery == 'function'){
        $(document).ready(function() {
            $('body').off('change', '.station_status[id*=station_status_wbst_]');
            $('body').on('change', '.station_status[id*=station_status_wbst_]', function () {
                var idx = $(this).attr('id').replace('station_status_', '');
                oTable[idx].fnFilter('');
            });

            // widget_indicator_block
            $('body').off('click', '[id*="custom_datatable_wbst_"] tbody tr');
            $('body').on('click', '[id*="custom_datatable_wbst_"] tbody tr', function (e) {
                // Highlight selected row
                if ($(this).hasClass('selected')){
                // Click vao row dang dc select --> ko lam gi ca
                } else {
                    $(this).closest('tbody').find('tr').removeClass('selected');
                    $(this).addClass('selected');
                }

                var container = $(this).closest('.panel-body').find('.widget_indicator_block');
                var url = container.attr('data-url');
                var station_id = $(this).attr('data-id');
                if (!station_id){
                    return true;
                }
                var params = {
                    station_id: station_id,
                };
                url += '?' + $.param(params);
                container.load(url);

                // widget_graph_detail
                var container2 = $(this).closest('.panel-body').find('.widget_graph_detail');
                var url2 = container2.attr('data-url');
                var params2 = {
                    station_id: station_id,
                };
                url2 += '?' + $.param(params2);
                container2.load(url2);
            });
        });
        clearInterval(wbstInterval);
    }
}, 50);

if (typeof fnCustomDrawCallback_wbst == 'undefined') {
    function fnCustomDrawCallback_wbst() {
        if (typeof isLoadIndicatorBlock == 'undefined' || !isLoadIndicatorBlock) {
            var activedPanel = $("[id*='wbst-tab-'].active").first();
            if (activedPanel.length > 0) {
                var st = activedPanel.attr('id').replace('wbst-tab-', '');
                $('#custom_datatable_wbst_' + st).find('tbody tr:first').trigger('click');
            }
            isLoadIndicatorBlock = true;
        }
    }
}

function fnCustomServerData_wbst(sSource, aoData, fnCallback) {
    aoData.push({
        "name": 'area_id', "value": $('#global_area_id').val()
    });
    aoData.push({
        "name": 'province_id', "value": $('#global_province_id').val()
    });
}