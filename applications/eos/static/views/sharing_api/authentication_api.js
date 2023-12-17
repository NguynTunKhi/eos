//--By TheVH, who is newbie here 2020--

var array_btn_detail = {
        'wastewater_station':null,
        'surfacewater_station':null,
        'ambientair_station':null,
        'stackemission_station':null,
        'undergroundwater_station':null,
        'data_1h':[{'station_id':'Mã trạm*'},{'from_data':'Từ ngày'},{'to_data':'Tời ngày'}],
        'data_1d':[{'station_id':'Mã trạm*'},{'from_data':'Từ ngày'},{'to_data':'Tời ngày'}],
        'data_1m':[{'station_id':'Mã trạm*'},{'from_data':'Từ ngày'},{'to_data':'Tời ngày'}],
        'detail_stations1':[{'station_id':'Mã trạm*'}],
        'detail_stations4':[{'station_id':'Mã trạm*'}],
        'aqi_ngay':[{'station_id':'Mã trạm*'}]
        }

$(document).ready(function() {
    getting_list_api()
    $('#btn_save').click(function(e) {
        save_data();
    });
    on_change_user()

    $('#btn_copy').click(function() {
        copy_token();
    });
    check_unchecked_all();

    $('#close_modal_btn').click(function(){
    $('#modal-form').css('display','none');
    $("#table-detail > tbody").empty();
    })
});

function handleClickDetail(e){
    var service_key = e.id.replace('_btn','')
    $('#modal-form').css('display','block')

    adding_node_popup();
    var url = $("#table-detail").attr("data-url");
    $.ajax({
      type: "POST",
      url: url,
      data: {service_key},
      success: function(rs) {
      var data_detail = rs.data[0]
          data_detail['token'] = $('#token').val()
          data_detail['params'] = array_btn_detail[service_key]
          $.each(data_detail, function( key, value ) {
          if(key!='key'){
          if(key!='params'){
            var html = '<td style="text-align: left">'+ app.translate(`${key}_fs`) +'</td>' + '<td style="text-align: left;width: 100px;overflow: hidden;text-overflow: ellipsis;  white-space: nowrap; ">'+ value +'</td>';
            $('#table-detail > tbody').append('<tr>' + html + '</tr>')
            } else {
            if(value){
            var params_text = []
            value.forEach(function(item){
            $.each(item,function(k,v){
            params_text.push(`<div>${k}: -${v}</div>`)
            })
            })
            var html = '<td style="text-align: left">'+ app.translate(`${key}_fs`) +'</td>'+'<td style="text-align:left">' + params_text.join(" ") +'</td>'
            $('#table-detail > tbody').append('<tr>' + html + '</tr>')
            }
            }
             }
        });
      },
    });
}

function save_data() {
    var data = {'list_authen': ''};
    var checked_list = []
    $('input[name="api-checked"]:checked').each(function() {
           checked_list.push(this.value);
    });
    data['list_authen'] = checked_list.join(';');
    data['user_id'] = $('#user_id').val();
    data['token'] = $('#token').val();
    data['department_name'] = $('#department_name').val();
    if (!data['department_name'] || !data['user_id'] || !data['user_id'] || !data['user_id']) {
        message('Tên đơn vị, Người dùng là bắt buộc nhập!', 1000, 'error')
        return
    }
    $.ajax({
        type:'POST',
        url: $('#btn_save').attr('data-url'),
        dataType:'json',
        data: data,
        success:function(rs){
            message('Lưu thành công!',1000,'success')
        }
    })
}

function copy_token() {
 var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($("#token").val()).select();
  document.execCommand("copy");
  $temp.remove();
  message('Đã copy vào clipboard!',1000,'success')
}

function getting_list_api(){
    var url = $("#table-auth-api").attr("data-url");
    $.ajax({
      type: "POST",
      url: url,
      data: {},
      success: function(rs) {
        $.each(rs['aaData'], function( index, value ) {
              var html = '<td>'+ value[0] +'</td>' + '<td>'+ value[1] +'</td>'+ '<td>'+ value[2] +'</td>' + '<td>'+ value[3] +'</td>' +   '<td style="text-align: center;cursor: pointer">'+'<button onclick="handleClickDetail(this)" id="'+ value[4]+"_btn"    +'" type="button" class="btn btn-default" data-toggle="tooltip" data-placement="top" title="Chi tiết sử dụng!" data-original-title="Tooltip on top">'+'<i class="fa fa-info-circle" ></i>'+'</button>'+'</td>'  + '<td style="text-align: center">'+ '<input type="checkbox" name="api-checked" value="' + value[4] + '">' +'</td>';
             $('#table-auth-api > tbody').append('<tr>' + html + '</tr>')
        });
      }
    });
}

function on_change_user() {
    $('#user_id').change(function(e) {
        $('#token').val('');
        $.ajax({
        type: "POST",
         url: $(this).attr('data-url'),
         data: {'user_id': $(this).val()},
         success: function(rs) {
            if (rs.success) {
                $('#token').val(rs.data.token);
                var checked_list = rs.data.list_authen
                $('input[name="api-checked"]').each(function() {
                    this.checked = checked_list.includes(this.value);
                });
                $('#department_name').val(rs.data.department_name)
            }
        }
    });
    });
}

function check_unchecked_all() {
    $("#chk-api-all").change(function() {
        $('input[name="api-checked"]').not(this).prop('checked', this.checked);
    });
}

function message(text,time_out,type){
    toastr.options={
        timeOut:time_out,
        positionClass:'toast-top-center'
    }
    toastr[type](text,'Thông báo!');
}

function goBack(){
    window.history.back();
}

function adding_node_popup(){
}
