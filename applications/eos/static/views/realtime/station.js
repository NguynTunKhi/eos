$(document).ready(function() {
    loadDataTableForPage();

    setInterval(function() {
        oTable[0].fnFilter('');
    }, 180*1000);

    // 300*1000
    // $('body').on('change', '#dt0_station_id', function (e) {
        // oTable[0].fnFilter('');
    // });



    $('#cbbAddedColumns_chosen').attr('style', 'width: 100%; margin-bottom: 5px; margin-top: 5px;')
//    $('#custom_datatable_0 thead tr').append('<th class="quick_view" colspan="3" style="width: 8%">Quick view</th>');
   // $('#real_time tr').append('<th class="quick_view" colspan="3" style="width: 8%">Quick view</th>');
    $('body').on('click', '#check_indicator', function (e) {
        if(e.target.checked){
            console.log(e.target.checked)
            $('#cbbAddedColumns option').prop('selected', true);
            $('#cbbAddedColumns').trigger("change");
            $('#cbbAddedColumns').trigger('chosen:updated');

        } else {
            console.log(e.target.checked)
            $('#cbbAddedColumns option:selected').removeAttr('selected');
            $('#cbbAddedColumns').trigger("change");
            $('#cbbAddedColumns').trigger('chosen:updated');
        }
    });

    $('body').on('change', '#dt0_province_id', function (e) {
        var url = $(this).data('url');
        var data = {};


        app.postAjax({
            url: url,
//            data: {filter_value : $(this).val(),station_type : $('#dt0_station_type').val()},
//            data: {filter_value:$('#dt0_province_id').val().trim() + ';' +  $('#dt0_station_type').val()},
            data: {filter_value:$('#dt0_province_id').val().trim(), station_type: $('#dt0_station_type').val()},
            callback: function (res) {
                if (res.success) {
                    $('#dt0_station_id').html(res.html);
                    $('#dt0_station_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });


    
    $('body').on('change', '#dt0_area_id', function (e) {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {filter_value : $(this).val(),station_type : $('#dt0_station_type').val()},
            
            callback: function (res) {
                if (res.success) {
                    $('#dt0_station_id').html(res.html);
                    $('#dt0_station_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('body').on('change', '#dt0_station_id', function (e) {
        // $('.btn-primary').onclick;
        var url = $(this).data('url');
        var station_type = $('#dt0_station_type').val();
        app.postAjax({
            url: url,
            data: {station_id : $(this).val(),station_type : $('#dt0_station_type').val()},

            callback: function (res) {
                if (res.success) {
                    $('#cbbAddedColumns').html(res.html);
                    $('#cbbAddedColumns').trigger("change");
                    $('#cbbAddedColumns').trigger("chosen:updated");

                    var idx = $(this).data('forDT');
                    if (idx == undefined){
                        idx = 0;
                    }
                    oTable[idx].fnFilter();
                } else {
                    app.showError(res.message);
                }
            }
        });


    });
});

function loadDataTableForPage() {
    var aoColumns = [
        {'sWidth' : '2%'},
        {'sWidth' : '2%'},
        {'sWidth' : '2%'},
        {'sWidth' : '2%'},
        {'sWidth' : '2%'},
        {'sWidth' : '15%'},
        {'sWidth' : '8%'},
    ];

    var aoClass = ['', '', 'text-left'];
    var sDom = "<'row horizontal-scroll't><'clear'><'row bottom' <'col-sm-6 text-left' li><'col-sm-6 text-right' p>><'clear'>";
    loadDataTable({
        aoColumns: aoColumns,
        aoClass: aoClass,
        sDom: sDom,
    });
    
    return true;
}