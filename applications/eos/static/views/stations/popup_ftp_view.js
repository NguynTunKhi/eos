var iTable = null;

var FTP_VIEW_TYPE_DIR = "directory";
var FTP_VIEW_TYPE_FILE = "file";

var cols = [
  {
    data: "t",
    sWidth: "5%",
    bSort: false,
    render: function (val) {
      if (val == "d")
        return `<i class='fa fa-folder' style='color: #FBDB79; font-size: 19px;'></i>`;
      return `<i class='fa fa-file-text-o'></i>`;
    },
  },
  {
    data: "n",
    sWidth: "40%",
    bSortable: false,
    render: function (val, m, r) {
      if (r["t"] == "f")
        return `<a target ='_blank' filename=${val} >${val}</a>`;
      return `<a onclick=go_to_folder("${val}")>${val}</a>`;
    },
  },
  {
    data: "s",
    sWidth: "25%",
    bSortable: false,
    render: function (val) {
      if (val) {
        return `${val}B`;
      }
      return "";
    },
  },
  { data: "ts", sWidth: "25%", bSortable: true },
  {
    data: "file_path",
    sWidth: "5%",
    bSortable: true,
    render: function (val, m, r) {
      filePath = r["file_path"];
      fileName = r["file_name"];
      if (r["view_type"] == FTP_VIEW_TYPE_FILE && r["t"] == "f") {
        return `<input name="ftp-file-item" type="checkbox" file_name=${fileName} onchange="ftpSelectFileOnChange(this)"
                value=${filePath}>`;
      } else if (r["view_type"] == FTP_VIEW_TYPE_DIR) {
        return `<input name="ftp-file-item" type="checkbox" file_name=${fileName} onchange="ftpSelectFileOnChange(this)"
                value=${filePath}>`;
      }
      return ``;
    },
  },
];

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
  bSort: false, //Cho ph�p s?p x?p
  bFilter: true, //S? d?ng b? l?c d? li?u(?n/hi?n thu?c t�nh t�m ki?m)
  sDom: "<'row middle ftp-file-table't><'clear'><'row bottom' <'col-sm-6 text-left no-padding' li><'col-sm-6 text-right no-padding' p>><'clear'>", //�?nh nghia css cho c�c ph?n c?a b?ng
  bDeferRender: true,
  oLanguage: {
    sZeroRecords: app.translate("JS_DT_NO_RECORD"),
    sInfoEmpty: "",
    sInfo:
      app.translate("JS_DT_DISPLAY") +
      " _START_ - _END_ (" +
      app.translate("JS_DT_IN") +
      " _TOTAL_)",
    sInfoFiltered: "(Filter _MAX_ from results)",
    sInfoPostFix: "",
    sSearch: app.translate("JS_DT_SEARCH"),
    sLengthMenu: "_MENU_",
    sUrl: "",
    oPaginate: {
      sFirst: app.translate("JS_DT_FIRST"),
      sPrevious: app.translate("JS_DT_PREVIOUS"),
      sNext: app.translate("JS_DT_NEXT"),
      sLast: app.translate("JS_DT_LAST"),
    },
  },
};

$(document).ready(function () {
  load_table();
  $("#btn-ftp-back").click(function () {
    if ($("#m-folder").val() != "/" && iTable) {
      go_to_folder("..");
    }
  });
  $("#btn-ftp-enter").click(function () {
    if ($("#m-folder").val() != "/" && iTable) {
      go_to_folder($("#m-folder").val());
    }
  });

  $("#btn_select_data_folder").click(function () {
    folderPath = $("#m-folder").val();
    ftpViewType = $("#ftp_view_type").val();
    let elements = document.getElementsByName("ftp-file-item");
    fileName = "";
    for (let i = 0; i < elements.length; i++) {
      if (elements[i].checked == true) {
        folderPath = elements[i].value;
        if (ftpViewType == FTP_VIEW_TYPE_FILE) {
          fileName = elements[i].getAttribute("file_name");
        }
      }
    }
    // set data for data_folder in form view
    if (ftpViewType == FTP_VIEW_TYPE_FILE) {
      $("#form-ftp-file_path").val(`${folderPath}`);
    }
    if (ftpViewType == FTP_VIEW_TYPE_DIR) {
      $("#form-ftp-folder-path").val(folderPath);
    }
    $("#btn_cancel").trigger("click");
  });
});

function ftpSelectFileOnChange(thisData) {
  let elements = document.getElementsByName("ftp-file-item");
  for (let i = 0; i < elements.length; i++) {
    if (elements[i] == thisData) {
      continue;
    }
    elements[i].checked = false;
  }

  console.log("done");
}

function go_to_folder(folder) {
  $("#m-folder").attr("v-folder", folder);
  if (iTable) {
    iTable.fnFilter(folder);
  }
}

function load_table() {
  $table = $("#custom_datatable_popup_ftp_viewer");
  var station_id = $("#hf-station-id").val();
  var options = $.extend(tb_options, {
    bOrder: [[3, "desc"]],
    sAjaxSource: $table.attr("data-url"),
    fnServerData: function (sSource, aoData, fnCallback) {
      aoData.push({ name: "station_id", value: station_id });
      aoData.push({ name: "folder", value: $("#m-folder").val() });
      aoData.push({ name: "vFolder", value: $("#m-folder").attr("v-folder") });
      $("#custom_datatable_popup_ftp_viewer tbody").empty();
      $.post(sSource, aoData, function (data) {
        $("#m-folder").val(data.folder);
        fnCallback(data);
      });
    },
    columns: cols,
  });
  $table.DataTable().clear().destroy();
  iTable = $table.dataTable(options);
}
