var iTable = null

var cols = [
    { data: 't', 'sWidth' : '5%', 'bSort' : false,
    render: function(val) {
        if (val == 'd')
            return `<i class='fa fa-folder' style='color: #FBDB79; font-size: 19px;'></i>`
        return `<i class='fa fa-file-text-o'></i>`
    }},
    { data: 'n', 'sWidth' : '45%', 'bSortable' : false,
        render: function(val, m, r) {
            if (r['t'] == 'f')
                return `<a target ='_blank' onclick=download_file(this) filename=${val} data-url=stations/download>${val}</a>`
            return `<a onclick=go_to_folder("${val}")>${val}</a>`
        }
    },
    { data: 's', 'sWidth' : '25%', 'bSortable' : false,
        render: function(val) {
            if (val){ return `${val}B`}
            return ''
        }
    },
    { data: 'ts', 'sWidth' : '25%', 'bSortable' : true,},
]

var tb_options = {
    sAjaxDataProp: "data",
    iDisplayLength: 1000,
    aLengthMenu: [15, 30, 50, 100, 200, 300, 1000],
    bServerSide: true,
    bDestroy: true,
    bInfo: true,
    bAutoWidth: false,
    stateSave: false,
    paging: false,
    bSort: false,//Cho ph�p s?p x?p
    bFilter: true,//S? d?ng b? l?c d? li?u(?n/hi?n thu?c t�nh t�m ki?m)
    sDom: "<'row middle't><'clear'><'row bottom' <'col-sm-6 text-left no-padding' li><'col-sm-6 text-right no-padding' p>><'clear'>",//�?nh nghia css cho c�c ph?n c?a b?ng
    bDeferRender: true,
    oLanguage: {
        "sZeroRecords": app.translate("JS_DT_NO_RECORD"),
        "sInfoEmpty": "",
        "sInfo": app.translate("JS_DT_DISPLAY") + " _START_ - _END_ (" + app.translate("JS_DT_IN") +" _TOTAL_)",
        "sInfoFiltered": "(Filter _MAX_ from results)",
        "sInfoPostFix": "",
        "sSearch": app.translate("JS_DT_SEARCH"),
        "sLengthMenu": "_MENU_",
        "sUrl": "",
        "oPaginate": {
            "sFirst": app.translate("JS_DT_FIRST"),
            "sPrevious": app.translate("JS_DT_PREVIOUS"),
            "sNext": app.translate("JS_DT_NEXT"),
            "sLast": app.translate("JS_DT_LAST")
        }
    }
}

$(document).ready(function () {
    load_table()
    $('#btn-ftp-back').click(function() {
        if ($('#hf-f').val() !== $('#m-folder').val() && iTable)
            go_to_folder('..')
    })
    $('#btn-ftp-enter').click(function() {
        if ($('#m-folder').val() != "/" && iTable) {
            go_to_folder($('#m-folder').val())
        }
    })
})




function go_to_folder(folder) {
    $('#m-folder').attr('v-folder', folder)
    if (iTable) {
        iTable.fnFilter(folder)
    }
}

function download_file(el){
    $el = $(el)
    var url = $el.attr('data-url')
    var filename = $el.attr('filename')
    var station_id = $('#hf-station-id').val()
    var folder = $('#m-folder').val()
    window.location = `/eos/${url}?filename=${filename}&station_id=${station_id}&folder=${folder}`
}

function load_table() {
    $table = $('#custom_datatable_0')
    var station_id = $('#hf-station-id').val()
    var options = $.extend(tb_options, {
        bOrder: [[ 3, "desc" ]],
        sAjaxSource: $table.attr('data-url'),
        fnServerData: function(sSource, aoData, fnCallback) {
            aoData.push({name: "station_id", value: station_id})
            aoData.push({name: "folder", value: $('#m-folder').val()})
            aoData.push({name: "vFolder", value: $('#m-folder').attr('v-folder')})
            $('#custom_datatable_0 tbody').empty()
            $.post(sSource, aoData, function(data) {
                $('#m-folder').val(data.folder)
                fnCallback(data)
            })

        },
        columns: cols
    })
    $table.DataTable().clear().destroy();
    iTable = $table.dataTable(options)
}
