var validator2 = null;
var validator7 = null;
var validator8 = null;
var validatorHaveKind_8 = null;

var FTP_VIEW_TYPE_DIR = "directory";
var FTP_VIEW_TYPE_FILE = "file";

$(document).ready(function () {
  // Validate form
  // app.validateForm("form#frmMain");
  validator = $("form#frmMain").validate({
    rules: {
      station_code: "required",
      station_name: "required",
      area_id: "required",
      longitude: {
        required: true,
        number: true,
        range: [100, 112],
      },
      latitude: {
        required: true,
        number: true,
        range: [7, 24],
      },
      province_id: "required",
      frequency_receiving_data: "required",
      time_count_offline: "required",
      station_type: "required",
      order_in_area: "digits",
      interval_scan: {
        required: true,
        digits: true,
      },
      retry: {
        required: true,
        digits: true,
      },
      email: "email",
      phone: "phone",
      //            data_server: 'required',
      //            data_folder: 'required',
      data_server_port: "digits",
      username: "username",
      //            pwd: 'required',
      //            type_logger: 'required'
    },
    messages: {
      station_code: app.translate("LBL_INPUT_MANDATORY_FIELD"),
      station_name: app.translate("LBL_INPUT_MANDATORY_FIELD"),
      province_id: app.translate("LBL_INPUT_MANDATORY_FIELD"),
      station_type: app.translate("LBL_INPUT_MANDATORY_FIELD"),
      order_in_area: app.translate("LBL_INPUT_MANDATORY_FIELD"),
      email: app.translate("LBL_INPUT_EMAIL_FIELD"),
      phone: app.translate("LBL_INPUT_PHONE_FIELD"),
      data_server: app.translate("LBL_INPUT_MANDATORY_FIELD"),
      data_folder: app.translate("LBL_INPUT_MANDATORY_FIELD"),
      frequency_receiving_data: app.translate("LBL_INPUT_INTEGER"),
      time_count_offline: app.translate("LBL_INPUT_INTEGER"),
      data_server_port: app.translate("LBL_INPUT_INTEGER"),
      longitude: {
        required: app.translate("LBL_INPUT_MANDATORY_FIELD"),
        number: app.translate("LBL_INPUT_INTEGER"),
        range: app.translate("LBL_INPUT_RANGE"),
      },
      latitude: {
        required: app.translate("LBL_INPUT_MANDATORY_FIELD"),
        number: app.translate("LBL_INPUT_INTEGER"),
        range: app.translate("LBL_INPUT_RANGE"),
      },
    },
  });
  validator2 = $("form#frmTabIndicator").validate({
    rules: {
      indicator: {
        required: true,
      },
      indicator_name_mapping: {
        required: true,
      },
      convert_rate: {
        required: true,
      },
      tendency: {
        required: true,
        number: true,
      },
      preparing: {
        required: true,
        number: true,
        greaterOrEqual: "tendency",
      },
      exceed: {
        required: true,
        number: true,
        greaterOrEqual: "preparing",
      },
      //            lrv: {
      //                required: function () {
      //                    return ($('#cbbEquipment_chosen').val() != '');
      //                },
      //                number: true,
      //            },
      //            urv: {
      //                required: function () {
      //                    return ($('#cbbEquipment_chosen').val() != '');
      //                },
      //                number: true,
      //                greaterOrEqual: 'lrv',
      //            },
      qcvn_min: {
        number: true,
      },
      qcvn_max: {
        number: true,
        greaterOrEqual: "qcvn_min",
      },
      convert_rate: {
        required: true,
        number: true,
      },
      // qcvn_code: {
      //     required: true,
      // },
      // qcvn_detail_const_area_value_1: {
      //     required: true,
      //     number: true,
      // },
      // qcvn_detail_const_area_value_2: {
      //     required: true,
      //     number: true,
      // },
    },
    messages: {},
  });
  validator7 = $("form#frmTab7").validate({
    rules: {
      continous_equal_value: {
        number: true,
      },
    },
    messages: {},
  });

  validator8 = $("form#frmTabQCVN").validate({
    rules: {
      cbbQCVN_8: {
        required: true,
      },
      // qcvn_detail_const_area_value_1: {
      //     required: true,
      //     number: true,
      // },
      // qcvn_detail_const_area_value_2: {
      //     required: true,
      //     number: true,
      // },
    },
    messages: {},
  });

  validatorHaveKind_8 = $("form#frmTabQCVN").validate({
    rules: {
      cbbQCVN_TYPE_CODE_8: {
        required: true,
      },
    },
    messages: {},
  });

  var recordId = $("#hfStationId").val();
  if (recordId) {
    loadDataTableForPage();
    loadDataTableForPage_Indicator();
    loadDataTableForPage_camera();
    loadDataTableForPage_auto_adjust();
    loadDataTableForPage_DataCommand();
    cbb_logger_type_change();
  }
  switch_transfer_type();
  $("#btnSave").click(function () {
    var dt0_to_date = $("#stations_last_time");
    var toDate = new Date(dt0_to_date.val());
    var maxDate = new Date();
    const myTimeZone = 7;
    maxDate.setTime(maxDate.getTime() + myTimeZone * 60 * 60 * 1000);
    var minDate = new Date(dt0_to_date.val());

    if (toDate > maxDate) {
      app.showError(
        app.translate("ERR_Day_Input_Station_Last_Time_Max_Exceed")
      );
      return false;
    }
    if (!validateForm()) {
      app.focusToFirstError();
      return false;
    }
    app.showConfirmBox({
      content: app.translate("JS_MSG_CONFIRM_SAVE"),
      callback: function () {
        $("#frmMain").submit();
      },
    });
  });
  $("body").on("change", "#cbb-transfer-type", function (e) {
    switch_transfer_type();
  });

  $("body").on("click", "#btn-mqtt-check", function (e) {
    check_connect_mqtt({
      data: { client_id: $("input#stations_mqtt_client_id").val() },
      url: $(this).attr("data-url"),
    });
  });

  $("body").on("change", "#cbbIndicatorId", function (e) {
    var indicator_id = $(this).val();
    var qcvn_kind_id = $("#e").val();
    var qcvn_id = $("#cbbQCVN_AJAX").val();
    var cons_1 = $("#cbbQCVN_heso_1").val();
    var cons_2 = $("#cbbQCVN_heso_2").val();

    $("#txtTendency").val("");
    $("#txtPreparing").val("");
    $("#txtExceed").val("");
    var url = $(this).data("url");
    var data = {
      indicator_id: indicator_id,
      qcvn_id: qcvn_id,
      qcvn_kind_id: qcvn_kind_id,
      cons_1: cons_1,
      cons_2: cons_2,
    };
    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          $("#txtTendency").val(res.tendency_value);
          $("#txtPreparing").val(res.preparing_value);
          $("#txtExceed").val(res.exceed_value);
          $("#indicator_name_mapping").val(res.source_name);

          $("#qcvn_detail_min_value").val(res.qcvn_min_value_indicator);
          $("#qcvn_detail_max_value").val(res.qcvn_max_value_indicator);
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  const_value = $("#cbbQCVN_8 option:selected").attr("value_const");
  if (const_value == 1) {
    $("#qcvn_detail_const_area_value_1").attr("type", "number");
    $("#qcvn_detail_const_area_value_2").attr("type", "number");
    $("#qcvn_detail_const_area_value_3").attr("type", "number");
    $("#lbl_qcvn_detail_const_area_value_type").attr(
      "style",
      "Display: block;"
    );
    $("#lbl_qcvn_detail_const_area_value_1").attr("style", "Display: block;");
    $("#lbl_qcvn_detail_const_area_value_2").attr("style", "Display: block;");
    $("#lbl_qcvn_detail_const_area_value_3").attr("style", "Display: block;");
  } else {
    $("#qcvn_detail_const_area_value_1").attr("type", "hidden");
    $("#qcvn_detail_const_area_value_2").attr("type", "hidden");
    $("#qcvn_detail_const_area_value_3").attr("type", "hidden");
    $("#lbl_qcvn_detail_const_area_value_type").attr(
      "style",
      "Display: block;"
    );
    $("#lbl_qcvn_detail_const_area_value_1").attr("style", "Display: none;");
    $("#lbl_qcvn_detail_const_area_value_2").attr("style", "Display: none;");
    $("#lbl_qcvn_detail_const_area_value_3").attr("style", "Display: none;");
  }
  var temp = false;
  $("body").on("change", "#cbbQCVN_8", function (e) {
    $(".validationErrorContainer").attr("style", "Display: none;");
    var const_val = $("#cbbQCVN_8 option:selected").attr("value_const");
    var qcvn_id = $(this).val();
    var url = $(this).data("url");
    var data = { qcvn_id: qcvn_id, station_id: $("#hfStationId").val() };

    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          $("#cbbQCVN_TYPE_CODE_8")
            .empty()
            .append($('<option value=""></option>').text("-- Chọn loại --"));
          $("#cbbIndicatorId")
            .empty()
            .append(
              $('<option value=""></option>').text("-- Chọn thông số --")
            );
          $.each(res.type_code, function (key, value) {
            qcvn_type_code = value.qcvn_type_code;
            if (qcvn_type_code == "") {
              temp = true;
            } else {
              temp = false;
            }
          });
          if (res.qcvn_details.length == 0) {
            $("#qcvn_detail_const_area_value_1").attr("type", "hidden");
            $("#qcvn_detail_const_area_value_2").attr("type", "hidden");
            $("#qcvn_detail_const_area_value_3").attr("type", "hidden");
            $("#lbl_qcvn_detail_const_area_value_type").attr(
              "style",
              "Display: none;"
            );
            $("#lbl_qcvn_detail_const_area_value_1").attr(
              "style",
              "Display: none;"
            );
            $("#lbl_qcvn_detail_const_area_value_2").attr(
              "style",
              "Display: none;"
            );
            $("#lbl_qcvn_detail_const_area_value_3").attr(
              "style",
              "Display: none;"
            );
            $("#cbbQCVN_TYPE_CODE_8_chosen").attr("style", "Display: none;");
          } else {
            $.each(res.qcvn_details, function (key, value) {
              var value_option = value.id;
              var text = value.qcvn_kind != null ? value.qcvn_kind : "-";
              $("#cbbQCVN_TYPE_CODE_8").append(
                $("<option></option>")
                  .attr("value", value_option.toString())
                  .text(text)
              );
            });

            $("#cbbQCVN_TYPE_CODE_8").chosen().trigger("chosen:updated");
            if (const_val == 1) {
              $("#qcvn_detail_const_area_value_1").attr("type", "number");
              $("#qcvn_detail_const_area_value_2").attr("type", "number");
              $("#qcvn_detail_const_area_value_3").attr("type", "number");
              $("#lbl_qcvn_detail_const_area_value_type").attr(
                "style",
                "Display: block;"
              );
              $("#lbl_qcvn_detail_const_area_value_1").attr(
                "style",
                "Display: block;"
              );
              $("#lbl_qcvn_detail_const_area_value_2").attr(
                "style",
                "Display: block;"
              );
              $("#lbl_qcvn_detail_const_area_value_3").attr(
                "style",
                "Display: block;"
              );
            } else {
              $("#qcvn_detail_const_area_value_1").attr("type", "hidden");
              $("#qcvn_detail_const_area_value_2").attr("type", "hidden");
              $("#qcvn_detail_const_area_value_3").attr("type", "hidden");
              $("#lbl_qcvn_detail_const_area_value_type").attr(
                "style",
                "Display: block;"
              );
              $("#lbl_qcvn_detail_const_area_value_1").attr(
                "style",
                "Display: none;"
              );
              $("#lbl_qcvn_detail_const_area_value_2").attr(
                "style",
                "Display: none;"
              );
              $("#lbl_qcvn_detail_const_area_value_3").attr(
                "style",
                "Display: none;"
              );
            }

            $("#cbbQCVN_TYPE_CODE_8_chosen").attr("style", "Display: block;");
          }

          $.each(res.indicators, function (key, value) {
            var value_option = value.id;
            var text = value.id != null ? value.indicator : "-";
            $("#cbbIndicatorId").append(
              $("<option></option>")
                .attr("value", value_option.toString())
                .text(text)
            );
          });
          $("#cbbIndicatorId").chosen().trigger("chosen:updated");
          $("#cbbIndicatorId_chosen").attr("style", "Display: block;");
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  $("body").on("change", "#cbbQCVN_TYPE_CODE", function (e) {
    var id = $(this).val();
    $("#qcvn_detail_min_value").val(1);
    $("#qcvn_detail_max_value").val(1);
    // $('#qcvn_detail_const_area_value').val('');
    var url = $(this).data("url");
    var data = { id: id };
    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          $("#qcvn_detail_min_value").val(
            Math.ceil(res.qcvn_detail.qcvn_min_value * 1.1 * 1.2)
          );
          $("#qcvn_detail_max_value").val(
            Math.ceil(res.qcvn_detail.qcvn_max_value * 1.1 * 1.2)
          );
          $("#qcvn_detail_const_area_value").val(
            res.qcvn_detail.qcvn_const_area_value
          );
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  // Add new Indicator to station
  $("body").on("click", "#btnLinkIndicatorToWaterStation", function (e) {
    if (!validator2.form()) return;
    var station_type = $(this).data("type");
    var data = {
      indicator: $("#cbbIndicatorId").val(),
      tendency: $("#txtTendency").val(),
      preparing: $("#txtPreparing").val(),
      exceed: $("#txtExceed").val(),
      station_id: $("#hfStationId").val(),
      station_name: $("#hfStationName").val(),
      equipment_id: $("#cbbEquipment").val(),
      equipment: $("#cbbEquipment option:selected").text(),
      equipment_lrv: $("#lrv").val(),
      equipment_urv: $("#urv").val(),
      qcvn_id: $("#cbbQCVN_8").val(),
      qcvn_kind_id: $("#cbbQCVN_TYPE_CODE_8").val(),
      qcvn_code: $("#cbbQCVN_8 option:selected").text(),
      qcvn_detail_type_code: $("#cbbQCVN_TYPE_CODE_8 option:selected").text(),
      qcvn_detail_const_area_value_1: $(
        "#qcvn_detail_const_area_value_1"
      ).val(),
      qcvn_detail_const_area_value_2: $(
        "#qcvn_detail_const_area_value_2"
      ).val(),
      qcvn_detail_const_area_value_3: $(
        "#qcvn_detail_const_area_value_3"
      ).val(),
      indicator_name_mapping: $("#indicator_name_mapping").val(),
      convert_rate: $("#convert_rate").val(),
      station_type: station_type,
    };

    var url = $(this).data("url");
    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          oTable[1].fnDraw();
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  $('body').on('click', '#btnUpdateListLinkStationIndicator', function (e) {
    var station_type = $(this).data('type');
    var data = {
        station_id: $('#hfStationId').val(),
        station_name: $("#hfStationName").val(),
        convert_rate: $("#convert_rate").val(),
        station_type: station_type,
    };
    var url = $(this).data('url');
    app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
            if (res.success) {
                oTable[1].fnDraw();
            } else {
                app.showError(res.message);
            }
        }
    });
})

  // Add new Indicator to station
  $("body").on("click", "#btnLinkIndicatorToWaterStation_8", function (e) {
    if (!validator8.form()) return;
    var length_cbbQCVN_TYPE_CODE_8 = $("#cbbQCVN_TYPE_CODE_8").children(
      "option"
    ).length;
    if (
      length_cbbQCVN_TYPE_CODE_8 > 1 &&
      $("#cbbQCVN_TYPE_CODE_8").val() == "" &&
      temp == false
    ) {
      $("#cbbQCVN_TYPE_CODE_8").formError(
        app.translate("LBL_INPUT_MANDATORY_FIELD")
      );
      $("#cbbQCVN_TYPE_CODE_8").focus();
      return false;
    } else {
      $(".validationErrorContainer").attr("style", "Display: none;");
    }
    var station_type = $(this).data("type");
    var data = {
      station_id: $("#hfStationId").val(),
      station_name: $("#hfStationName").val(),
      qcvn_id: $("#cbbQCVN_8").val(),
      qcvn_kind_id: $("#cbbQCVN_TYPE_CODE_8").val(),
      qcvn_code: $("#cbbQCVN_8 option:selected").text(),
      qcvn_detail_type_code: $("#cbbQCVN_TYPE_CODE_8 option:selected").text(),
      qcvn_detail_const_area_value_1: $(
        "#qcvn_detail_const_area_value_1"
      ).val(),
      qcvn_detail_const_area_value_2: $(
        "#qcvn_detail_const_area_value_2"
      ).val(),
      station_type: station_type,
    };
    // $('#cbbQCVN').attr("placeholder", $(this).find(':selected').text('cbbQCVN_8'));

    var url = $(this).data("url");
    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          app.showNotification(res);
          var id = "tab-8";
          window.location.hash = id;
          location.reload();
          //oTable[1].fnDraw();
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  // Save Alarm info
  $("body").on("click", "#btnAddStationAlarm", function (e) {
    if (!validateFormAlarm()) return;
    var station_type = $(this).data("type");
    var data = {
      tendency_method_email: $("#tendency_method_email").prop("checked"),
      tendency_method_sms: $("#tendency_method_sms").prop("checked"),
      tendency_emails: $("#tendency_emails").val(),
      tendency_phones: $("#tendency_phones").val(),
      tendency_msg: $("#tendency_msg").val(),
      preparing_method_email: $("#preparing_method_email").prop("checked"),
      preparing_method_sms: $("#preparing_method_sms").prop("checked"),
      preparing_emails: $("#preparing_emails").val(),
      preparing_phones: $("#preparing_phones").val(),
      preparing_msg: $("#preparing_msg").val(),
      exceed_method_email: $("#exceed_method_email").prop("checked"),
      exceed_method_sms: $("#exceed_method_sms").prop("checked"),
      exceed_method_notification: $("#exceed_method_notification").prop(
        "checked"
      ),
      exceed_emails: $("#exceed_emails").val(),
      frequency_notify: $("#frequency_notify").val(),
      exceed_phones: $("#exceed_phones").val(),
      exceed_msg: $("#exceed_msg").val(),
      station_id: $("#hfStationId").val(),
      station_name: $("#hfStationName").val(),
      station_type: station_type,
    };
    var url = $(this).data("url");
    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
          //focus vao tab alarm
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  // Save Alarm info
  $("body").on("click", "#btnFileMapping", function (e) {
    if (!validateFormFileMapping()) return;
    var data = {
      station_id: $("#hfStationId").val(),
      file_mapping: $("#fileMapping").val(),
      file_mapping_desc: $("#fileMappingDesc").val(),
    };
    var url = $(this).data("url");
    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  $("body").on("click", "#btnSaveDatalogger", function (e) {
    var data = {
      station_id: $("#hfStationId").val(),
      logger_id: $("#logger_id_show").val(),
      logger_name: $("#logger_name_show").val(),
      station_name: $("#station_name").val(),
      type_logger: $("#cbbTypeLogger").val(),
    };
    if (
      ($("#logger_id_show").val() != "") &
      ($("#logger_name_show").val() != "") &
      ($("#cbbTypeLogger").val() != "")
    ) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res.success) {
            toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
            location.reload();
          } else {
            app.showError(res.message);
          }
        },
      });
    } else {
      //            app.showError(app.translate('LBL_INPUT_MANDATORY_FIELD'));
      if ($("#cbbTypeLogger").val() == "") {
        app.showError(app.translate("LBL_CBB_DATALOGGER_TYPE"));
      } else {
        app.showError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
      }
    }
  });
  $("body").on("click", "#btnCreateDatalogger", function (e) {
    var data = {
      station_id: $("#hfStationId").val(),
      logger_id: $("#logger_id").val(),
      logger_name: $("#logger_name").val(),
      type_logger: $("#cbbTypeLogger").val(),
      station_name: $("#station_name").val(),
    };
    if (
      ($("#logger_id").val() != "") &
      ($("#logger_name").val() != "") &
      ($("#cbbTypeLogger").val() != "")
    ) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res.success) {
            toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
            location.reload();
          } else {
            app.showError(res.message);
          }
        },
      });
    } else {
      if ($("#cbbTypeLogger").val() == "") {
        app.showError(app.translate("LBL_CBB_DATALOGGER_TYPE"));
      } else {
        app.showError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
      }
    }
  });

  try {
    if (
      $("#send_data_from_date_show").val() != "" &&
      typeof $("#send_data_from_date_show").val() != "undefined"
    ) {
      $("#send_data_from_date_show").val(
        $("#send_data_from_date_show")
          .val()
          .split("T")[0]
          .split("-")
          .join("/") +
          " " +
          $("#send_data_from_date_show")
            .val()
            .split("T")[1]
            .split(".")[0]
            .split(":")
            .slice(0, 2)
            .join(":")
      );
    }
  } catch (err) {
    console.log("undefined");
  }

  $("body").on("click", "#btnSaveSendData", function (e) {
    if ($("#send_data_from_date_show").val() == "") {
      $("#send_data_from_date_show").formError(
        app.translate("LBL_INPUT_MANDATORY_FIELD")
      );
      $("#send_data_from_date_show").focus();
      return false;
    } else {
      $(".validationErrorContainer").attr("style", "Display: none;");
    }

    var data = {
      station_id: $("#hfStationId").val(),
      status: $("#send_status_show option:selected").val(),
      time_send_data: $("#time_send_data_show").val(),
      from_date: new Date(
        new Date($("#send_data_from_date_show").val()) -
          new Date().getTimezoneOffset() * 60000
      ).toISOString(),
      file_format: $("input[name='repeatMode']:checked").val(),
      ftp_path: $("#ftp_path_show").val(),
      file_name: $("#file_name").val(),
      ftp_ip: $("#ftp_ip_show").val(),
      ftp_port: $("#ftp_port_show").val(),
      ftp_user: $("#user_ftp_show").val(),
      ftp_password: $("#password_show").val(),
    };
    if (
      ($("#time_send_data_show").val() != "") &
      ($("#ftp_ip_show").val() != "") &
      ($("#ftp_path_show").val() != "") &
      ($("#ftp_port_show").val() != "") &
      ($("#user_ftp_show").val() != "") &
      ($("#password_show").val() != "") &
      ($("#status_show").val() != "")
    ) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res.res) {
            toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
          } else {
            app.showConfirmBox({
              content: app.translate("LBL_FAIL_CONNECT_FTP"),
              cancel_callback: function () {
                $("#tabs a[href=#tab-3]").tab("show");
              },
            });
          }
        },
      });
    } else {
      app.showError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
    }
  });
  $("body").on("click", "#btnCreatSendData", function (e) {
    if ($("#send_data_from_date").val() == "") {
      $("#send_data_from_date").formError(
        app.translate("LBL_INPUT_MANDATORY_FIELD")
      );
      $("#send_data_from_date").focus();
      return false;
    } else {
      $(".validationErrorContainer").attr("style", "Display: none;");
    }
    var data = {
      station_id: $("#hfStationId").val(),
      status: $("#send_status option:selected").val(),
      time_send_data: $("#time_send_data").val(),
      from_date: new Date(
        new Date($("#send_data_from_date").val()) -
          new Date().getTimezoneOffset() * 60000
      ).toISOString(),
      file_format: $("input[name='repeatMode']:checked").val(),
      file_name: $("#file_name").val(),
      ftp_path: $("#ftp_path").val(),
      ftp_ip: $("#ftp_ip").val(),
      ftp_port: $("#ftp_port").val(),
      ftp_user: $("#user_ftp").val(),
      ftp_password: $("#password").val(),
    };
    if (
      ($("#time_send_data").val() != "") &
      ($("#ftp_ip").val() != "") &
      ($("#ftp_path").val() != "") &
      ($("#ftp_port").val() != "") &
      ($("#user_ftp").val() != "") &
      ($("#password").val() != "") &
      ($("#status").val() != "")
    ) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res.success) {
            toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
            location.reload();
          } else {
            app.showError(res.message);
          }
        },
      });
    } else {
      app.showError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
    }
  });

  $("body").on("click", "#btncheckFTP_SHOW", function (e) {
    var data = {
      ftp_path: $("#ftp_path_show").val(),
      user: $("#user_ftp_show").val(),
      password: $("#password_show").val(),
      ftp_ip: $("#ftp_ip_show").val(),
      ftp_port: $("#ftp_port_show").val(),
    };
    if (
      ($("#ftp_ip_show").val() != "") &
      ($("#ftp_path_show").val() != "") &
      ($("#ftp_port_show").val() != "") &
      ($("#user_ftp_show").val() != "") &
      ($("#password_show").val() != "")
    ) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res) {
            app.showConfirmBox({
              content: app.translate("LBL_SUCSESS_CONNECT"),
              callback: function () {},
            });
          } else {
            app.showError(app.translate("LBL_FAIL_CONNECT"));
          }
        },
      });
    } else {
      app.showError(app.translate("LBL_IN_PUT_ALL"));
    }
  });

  $("body").on("click", "#btnFTP_Connect", function (e) {

    if ($("#ftp_id").val() != "") {
      server = encodeURI($("#ftp_id").val());
    } else {
      server = encodeURI($("#ftp_id").val());
    }
    var data = {
      data_server: server,
      data_folder: $("#form-ftp-file_path").val(),
      station_id: $("#hfStationId").val(),
      username: $("#stations_username").val(),
      pwd: $("#stations_pwd").val(),
      data_server_port: $("#stations_data_server_port").val(),
      station_code: $("#stations_station_code").val(),
    };

    if (
      (($("#ftp_id").val() != "") |
        ($("#ftp_id").val() != "")) &
      ($("#form-ftp-file_path").val() != "") &
      ($("#stations_data_server_port").val() != "") &
      ($("#stations_username").val() != "") &
      ($("#stations_pwd").val() != "") &
      ($("#stations_station_code").val() != "")
    ) {
      var user = encodeURIComponent($("#stations_username").val());
      var pass = encodeURIComponent($("#stations_pwd").val());
      var server = "";
      if ($("#stations_data_server_public").val() != "") {
        server = encodeURI($("#ftp_id").val());
      } else {
        server = encodeURI($("#ftp_id").val());
      }
      var port = encodeURI($("#stations_data_server_port").val());
      var folder = encodeURI($("#form-ftp-file_path").val());
      var witdth = screen.width / 2;
      var heigh = screen.height / 2;
      var top = screen.height / 4;
      var left = screen.width / 4;

      console.log(user, pass, server, port, folder,$("#form-ftp-file_path").val(), $("#stations_username").val(),  $("#stations_pwd").val(), $("#ftp_id").val(), $("#ftp_id").val(), $("#stations_data_server_port").val())
      var url_link =
        "ftp://" + user + ":" + pass + "@" + server + ":" + port;
      var param =
        "width=" +
        witdth +
        ",height=" +
        heigh +
        ", top=" +
        top +
        ", left=" +
        left;

      var url = $(this).data("url");
        app.showConfirmBox({
          content: app.translate("FTP_SUCSESS_CONNECT"),
        });

      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res) {
            app.showConfirmBox({
              content: app.translate("FTP_SUCSESS_CONNECT"),
            });
          } else {
            app.showError(app.translate("FTP_FAIL_CONNECT"));
          }
        },
      });
    } else {
      app.showError(app.translate("LBL_IN_PUT_ALL"));
    }
  });

  $("body").on("click", "#btncheckFTP_SHOW2", function (e) {
    ftpID = $("#ftp_id").val();
    stationID = $("#hfStationId").val();
    stationDataFolder = $("#stations_data_folder").val();

    var data = {
      ftp_id: ftpID,
      station_id: stationID,
      data_folder: stationDataFolder,
    };
    if ((stationDataFolder != "") & (ftpID != "")) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res) {
            app.showConfirmBox({
              content: app.translate("LBL_SUCSESS_CONNECT"),
            });
          } else {
            app.showError(app.translate("LBL_FAIL_CONNECT"));
          }
        },
      });
    } else {
      app.showError(app.translate("LBL_IN_PUT_ALL"));
    }
  });

  $("body").on("click", "#btncheckFTP", function (e) {
    var data = {
      ftp_path: $("#ftp_path").val(),
      user: $("#user_ftp").val(),
      password: $("#password").val(),
      ftp_ip: $("#ftp_ip").val(),
      ftp_port: $("#ftp_port").val(),
    };
    if (
      ($("#ftp_ip").val() != "") &
      ($("#ftp_path").val() != "") &
      ($("#ftp_port").val() != "") &
      ($("#user_ftp").val() != "") &
      ($("#password").val() != "")
    ) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res) {
            app.showConfirmBox({
              content: app.translate("LBL_SUCSESS_CONNECT"),
              callback: function () {},
            });
          } else {
            app.showError(app.translate("LBL_FAIL_CONNECT"));
          }
        },
      });
    } else {
      app.showError(app.translate("LBL_IN_PUT_ALL"));
    }
  });

  $("body").on("click", "#btncheckFTP_station", function (e) {
    var data = {
      ftp_path: $("#stations_ftp_path").val(),
      user: $("#stations_ftp_user").val(),
      password: $("#stations_ftp_pwd").val(),
      ftp_ip: $("#stations_ftp_ip").val(),
      ftp_port: $("#stations_ftp_port").val(),
    };
    if (
      ($("#stations_ftp_path").val() != "") &
      ($("#stations_ftp_user").val() != "") &
      ($("#stations_ftp_pwd").val() != "") &
      ($("#stations_ftp_ip").val() != "") &
      ($("#stations_ftp_port").val() != "")
    ) {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res.success) {
            app.showConfirmBox({
              content: app.translate("LBL_SUCSESS_CONNECT"),
              callback: function () {},
            });
          } else {
            app.showError(app.translate("LBL_FAIL_CONNECT"));
          }
        },
      });
    } else {
      app.showError(app.translate("LBL_IN_PUT_ALL"));
    }
  });

  $("body").on("change", "#cbbTypeLogger", function (e) {
    loadDataTableForPage_DataCommand();
    $("#d-usr").val("");
    $("#d-pwd").val("");
    if ($("#logger_name").val() == "" && $("#cbbTypeLogger").val()) {
      $("#logger_name").val($("#cbbTypeLogger option:selected").text());
    }
    cbb_logger_type_change();
  });

  $("body").on("click", "#btnAddDataCommand", function (e) {
    var logger_type = $("#cbbTypeLogger").val();
    var fields = [
      "station_name",
      "logger_id",
      "logger_name",
      "type_logger",
      "command_name",
    ];
    if (!logger_type) {
      toastr["warning"](app.translate("LBL_IN_PUT_ALL"));
      return;
    }
    if (logger_type === "D_LOGGER") {
      fields.push(...["command_id", "command_content"]);
    } else if (logger_type === "INVENTIA") {
      fields.push(...["command_content", "r-ip", "r-usr", "r-pwd"]);
    } else if (logger_type === "ADAM" || logger_type == "BL") {
      fields.push(...["r-ip", "r-usr", "r-pwd", "ch", "slot"]);
    }

    var arr = $("#frmTab10").serializeArray();
    var data = {};
    $.each(arr, function (i, field) {
      if (fields.includes(field.name)) {
        data[field.name] = field.value;
      }
    });

    var is_empty = false;
    for (var inx = 0; inx < fields.length; inx++) {
      f = fields[inx];
      if (logger_type === "ADAM" && f === "r-usr") {
        continue;
      }
      if (data[f] === "" || data[f] === undefined) {
        is_empty = true;
      }
    }
    if (is_empty) {
      toastr["warning"](app.translate("LBL_IN_PUT_ALL"));
    } else {
      var url = $(this).data("url");
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res.success) {
            toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
            //                        loadDataTableForPage_DataCommand()
            $("#custom_datatable_10").show();
            oTable[10].fnDraw();
          } else {
            toastr["warning"](res.message);
          }
        },
      });
    }
  });

  // Check/Uncheck continous_equal --> textbox : Readonly or not
  $("body").on(
    "click",
    '#custom_datatable_auto_adjust tbody tr td [name="continous_equal"]',
    function (e) {
      if ($(this).prop("checked") == true) {
        $(this).siblings().attr("readonly", false);
      } else {
        $(this).siblings().attr("readonly", true);
      }
    }
  );

  $("body").on(
    "click",
    '#custom_datatable_auto_adjust tbody tr td [name="remove_with_indicator_check"]',
    function (e) {
      if ($(this).prop("checked") == true) {
        $(this).siblings().attr("readonly", false);
      } else {
        $(this).siblings().attr("readonly", true);
      }
    }
  );

  // Save Auto adjust info
  $("body").on("click", "#btnAutoAdjust", function (e) {
    if (!validator7.form()) {
      return false;
    }
    var rows = $("#custom_datatable_auto_adjust tbody tr");

    // Duyet tung row tr de lay gtri
    var i, tr;
    var params = {};

    for (i = 0; i < rows.length; i++) {
      param = {};
      tr = $(rows[i]);
      var equal0 = tr.find("[name='equal0']");
      var negative_value = tr.find("[name='negative_value']");
      var out_of_range = tr.find("[name='out_of_range']");
      var out_of_range_min = tr.find("[name='out_of_range_min']");
      var out_of_range_max = tr.find("[name='out_of_range_max']");
      var equipment_adjust = tr.find("[name='equipment_adjust']");
      var equipment_status = tr.find("[name='equipment_status']");
      var continous_equal = tr.find("[name='continous_equal']");
      var continous_equal_value = tr.find("[name='continous_equal_value']");
      var remove_with_indicator_check = tr.find(
        "[name='remove_with_indicator_check']"
      );
      var remove_with_indicator = tr.find("[name='remove_with_indicator']");
      var extraordinary_value_check = tr.find(
        "[name='extraordinary_value_check']"
      );
    
      var extraordinary_value = tr.find(
        "[name='extraordinary_value']"
      );
      var compare_value_check = tr.find(
        "[name='compare_value_check']"
      );

      var compare_value = tr.find(
        "[name='compare_value']"
      );

      var coefficient_data = tr.find(
        "[name='coefficient_data']"
      );

      var parameter_value = tr.find(
        "[name='parameter_value']"
      );



      if (equal0.length > 0) {
        param["equal0"] = equal0.first().prop("checked");
      }
      if (negative_value.length > 0) {
        param["negative_value"] = negative_value.first().prop("checked");
      }
      if (out_of_range.length > 0) {
        param["out_of_range"] = out_of_range.first().prop("checked");
      }
      if (out_of_range_min.length > 0) {
        param["out_of_range_min"] = out_of_range_min.first().val();
      }
      if (out_of_range_max.length > 0) {
        param["out_of_range_max"] = out_of_range_max.first().val();
      }
      if (equipment_adjust.length > 0) {
        param["equipment_adjust"] = equipment_adjust.first().prop("checked");
      }
      if (equipment_status.length > 0) {
        param["equipment_status"] = equipment_status.first().prop("checked");
      }
      if (continous_equal.length > 0) {
        param["continous_equal"] = continous_equal.first().prop("checked");
      }
      if (continous_equal_value.length > 0) {
        param["continous_equal_value"] = continous_equal_value.first().val();
        if (param["continous_equal"] == true) {
          if ($("#myselect").length > 0) {
            validator7.element("#myselect");
          }
          if (isNaN(parseInt(param["continous_equal_value"])) == true) {
            app.showError(app.translate("LBL_INPUT_INTEGER"));
            return;
          }
        }
      }
      if (remove_with_indicator_check.length > 0) {
        param["remove_with_indicator_check"] = remove_with_indicator_check
          .first()
          .prop("checked");
      }
      if (remove_with_indicator.length > 0) {
        param["remove_with_indicator"] = remove_with_indicator.first().val();
        if (param["remove_with_indicator_check"] == true) {
          if ($("#myselect").length > 0) {
            validator7.element("#myselect");
          }
        }
      }

      if (extraordinary_value_check.length > 0) {
        param["extraordinary_value_check"] = extraordinary_value_check
          .first()
          .prop("checked");
      }
      if (extraordinary_value.length > 0) {
        param["extraordinary_value"] = extraordinary_value.first().val();
        if (param["extraordinary_value_check"] == true) {
          if ($("#myselect").length > 0) {
            validator7.element("#myselect");
          }
        }
      }

      if (compare_value_check.length > 0) {
        param["compare_value_check"] = compare_value_check
          .first()
          .prop("checked");
      }
      if (compare_value.length > 0) {
        param["compare_value"] = compare_value.first().val();
      }

      if (coefficient_data.length > 0) {
        param["coefficient_data"] = coefficient_data.first().val();
          if ($("#myselect").length > 0) {
            validator7.element("#myselect");
          }
      }

      if (parameter_value.length > 0) {
        param["parameter_value"] = parameter_value.first().val();
          if ($("#myselect").length > 0) {
            validator7.element("#myselect");
          }
      }

      params[tr.data("id")] = param;
    }

    params = JSON.stringify(params);

    var data = {
      data: params,
    };
    var url = $(this).data("url");
    app.postAjax({
      url: url,
      data: data,
      callback: function (res) {
        if (res.success) {
          toastr["success"](app.translate("JS_MSG_SAVE_SUCCESS"));
        } else {
          app.showError(res.message);
        }
      },
    });
  });

  // Tab click
  $('a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
    var target = $(e.target).attr("href"); // activated tab
    if (target == "#tab-7") {
      oTable["auto_adjust"].fnFilter();
    }

    /*if (target == "#tab-3") {
            if (!$("#cbbQCVN_AJAX").length) {
                var id = 'tab-8';
                window.location.hash = id;
                app.showNotificationWithCallback({"content" : app.translate('MSG_STATION_NOT_CONFIG_QCVN')});
                // location.reload();
            }
        }*/
  });

  var hash = window.location.hash;
  $('.nav-tabs a[href="' + hash + '"]').tab("show");

  // Fill URV, LRV cua Equipment khi dropdown thay doi
  $("body").on("change", "#cbbEquipment", function (e) {
    var equip_id = $(this).val();
    var min = $(this).find(":selected").data("min");
    var max = $(this).find(":selected").data("max");

    // Set value to textbox
    $("#lrv").val(min);
    $("#urv").val(max);
  });

  // CSS lai dropdown QCVN o tab 3 indicator
  $(".chosen-container-single").css("width", "100%");

  $("#select_ftp_folder_path").click(function () {
    ftpID = $("#ftp_id").val();
    console.log("ftpID", ftpID);
    if (ftpID != "") {
      url = `/eos/stations/popup_ftp_view?ftp_id=${ftpID}&view_type=${FTP_VIEW_TYPE_DIR}`;
      $(this).attr("data-url", url);
    } else {
      app.showError(app.translate("LBL_IN_PUT_ALL"));
    }
    return;
  });

  $("#select_ftp_file_path").click(function () {
    ftpID = $("#ftp_id").val();
    if (ftpID != "") {
      url = `/eos/stations/popup_ftp_view?ftp_id=${ftpID}&view_type=${FTP_VIEW_TYPE_FILE}`;
      console.log("ftpID", ftpID);
      $(this).attr("data-url", url);
    } else {
      app.showError(app.translate("LBL_IN_PUT_ALL"));
    }
    return;
  });
});

function validateFormFileMapping() {
  return true;
}

function validateChooseFtpFolder() {}

// Validate form
function validateForm() {
  if (!validateMandatory()) return false;
  if (!validateBussiness()) return false;

  return true;
}

// Validate form Alarm
function validateFormAutoAdjust() {
  // Todo : can validate du lieu la so
  return true;
}

// Validate form Indicator
function validateForm2() {
  $("input, textarea, select").formError({ remove: true });
  if (!validateMandatory2()) return false;
  if (!validateType2()) return false;
  if (!validateBussiness2()) return false;

  return true;
}

// Validate form Alarm
function validateFormAlarm() {
  return true;
}

// Validate for fields mandatory
function validateMandatory() {
  //    if ()
  if (!validator.form()) return false;
  return true;
}

// Validate for bussiness of fields
function validateBussiness() {
  // Todo
  return true;
}

// Validate for fields mandatory
function validateMandatory2() {
  if (!$("#cbbIndicatorId").val().trim()) {
    $("#cbbIndicatorId").formError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
    $("#cbbIndicatorId").focus();
    return false;
  }
  if (!$("#txtTendency").val().trim()) {
    $("#txtTendency").formError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
    $("#txtTendency").focus();
    return false;
  }
  if (!$("#txtPreparing").val().trim()) {
    $("#txtPreparing").formError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
    $("#txtPreparing").focus();
    return false;
  }
  if (!$("#txtExceed").val().trim()) {
    $("#txtExceed").formError(app.translate("LBL_INPUT_MANDATORY_FIELD"));
    $("#txtExceed").focus();
    return false;
  }
  return true;
}

// Validate for type of fields
function validateType2() {
  return true;
}

// Validate for bussiness of fields
function validateBussiness2() {
  var tendency = parseFloat($("#txtTendency").val());
  var preparing = parseFloat($("#txtPreparing").val());
  var exceed = parseFloat($("#txtExceed").val());
  if (!(tendency < preparing && preparing < exceed)) {
    $("#txtTendency").formError(app.translate("Tendecy < Preparing < Exceed"));
    $("#txtTendency").focus();
    return false;
  }
  return true;
}

function resetForm() {
  // Todo
  return true;
}

function loadDataTableForPage() {
  var sAjaxSource = $("#custom_datatable_0").attr("data-url");
  var aoColumns = [
    { sWidth: "3%" },
    { sWidth: "25%" },
    { sWidth: "10%" },
    { sWidth: "15%" },
    { sWidth: "13%" },
    { sWidth: "10%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
  ];

  var aoClass = [
    "",
    "text-left",
    "",
    "text-left",
    "text-left",
    "",
    "text-right",
    "text-right",
    "",
  ];
  var sDom = "<'row middle't><'clear'>";
  loadDataTable({
    sAjaxSource: sAjaxSource,
    aoColumns: aoColumns,
    aoClass: aoClass,
    sDom: sDom,
  });

  return true;
}

function loadDataTableForPage_DataCommand() {
  $table = $("#custom_datatable_10");
  $table.hide();
  var sAjaxSource = $table.attr("data-url");
  var logger_type = $("#cbbTypeLogger").val();
  if (logger_type) {
    $table.show();
  }
  var aoColumns = [];
  var aoClass = [];

  $thead = $("#custom_datatable_10 thead tr th");
  $thead.each(function (index) {
    var id = $(this).attr("id");
    if (!["r-no", "r-del"].includes(id)) {
      $(this).remove();
    }
  });
  var cols = [];

  if (logger_type === "D_LOGGER") {
    cols = ["Command content", "Command title", "ID command"];
    aoColumns = [
      { sWidth: "3%", bSortable: false },
      { sWidth: "35%" },
      { sWidth: "35%" },
      { sWidth: "24%" },
      { sWidth: "8%" },
    ];
    ["", "text-left", "", "", ""];
  } else if (["ADAM", "BL"].includes(logger_type)) {
    aoColumns = [
      { sWidth: "3%", bSortable: false },
      { sWidth: "35%" },
      { sWidth: "24%" },
      { sWidth: "12%" },
      { sWidth: "12%" },
      { sWidth: "12%" },
      { sWidth: "8%" },
    ];
    aoClass = ["", "text-left", "", "", "", "", ""];
    cols = ["Slot", "CH", "Username", "IP", "Command title"];
  } else {
    cols = ["Command content", "Username", "IP", "Command title"];
    aoColumns = [
      { sWidth: "3%", bSortable: false },
      { sWidth: "35%" },
      { sWidth: "24%" },
      { sWidth: "18%" },
      { sWidth: "18%" },
      { sWidth: "8%" },
    ];
    aoClass = ["", "text-left", "", "", "", ""];
  }
  for (var inx = 0; inx < cols.length; inx++) {
    $("<th>" + app.translate(cols[inx]) + "</th>").insertAfter("#r-no");
  }

  var sDom = "<'row middle't><'clear'>";
  loadDataTable({
    sAjaxSource: sAjaxSource + "&type=" + logger_type,
    aoColumns: aoColumns,
    aoClass: aoClass,
    sDom: sDom,
    iTable: 10,
  });

  return true;
}

function loadDataTableForPage_Indicator() {
  var sAjaxSource = $("#custom_datatable_1").attr("data-url");
  var aoColumns = [
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
  ];

  var aoClass = [
    "",
    "text-left",
    "text-left",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "text-right",
    "",
    "",
  ];
  var sDom = "<'row middle horizontal-scroll't><'clear'>";
  loadDataTable({
    sAjaxSource: sAjaxSource,
    aoColumns: aoColumns,
    aoClass: aoClass,
    sDom: sDom,
    fnCustomServerData: function (sSource, aoData, fnCallback) {
      aoData.push({
        name: "station_id",
        value: $("#hfStationId").val(),
      });
    },
    iTable: 1,
  });

  return true;
}

function loadDataTableForPage_camera() {
  var sAjaxSource = $("#custom_datatable_3").attr("data-url");
  var aoColumns = [
    { sWidth: "5%" },
    { sWidth: "5%" },
    { sWidth: "30%" },
    { sWidth: "45%" },
    { sWidth: "5%" },
    { sWidth: "5%" },
    { sWidth: "5%" },
  ];

  var aoClass = ["", "", "text-left", "text-left", "", "", "", "", "", ""];
  var sDom = "<'row middle't><'clear'>";
  loadDataTable({
    sAjaxSource: sAjaxSource,
    aoColumns: aoColumns,
    aoClass: aoClass,
    sDom: sDom,
    iTable: 3,
  });

  return true;
}

function loadDataTableForPage_auto_adjust() {
  var sAjaxSource = $("#custom_datatable_auto_adjust").attr("data-url");
  var aoColumns = [
    { sWidth: "10%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
    { sWidth: "6%" },
    { sWidth: "6%" },
    { sWidth: "12%" },
    { sWidth: "12%" },
    { sWidth: "12%" },
    { sWidth: "14%" },
    { sWidth: "8%" },
    { sWidth: "8%" },
  ];

  var aoClass = ["", "", "", "", "", "", "", "","","","",""];
  var sDom = "<'row middle't><'clear'>";
  loadDataTable({
    sAjaxSource: sAjaxSource,
    aoColumns: aoColumns,
    aoClass: aoClass,
    sDom: sDom,
    fnCustomServerData: function (sSource, aoData, fnCallback) {
      aoData.push({
        name: "station_id",
        value: $("#hfStationId").val(),
      });
    },
    iTable: "auto_adjust",
  });

  return true;
}

function reloadDatatable_Equipment() {
  oTable[0].fnDraw();
}

function reloadDatatable_Camera() {
  oTable[3].fnDraw();
}

function reloadDatatable_DataCommand() {
  oTable[10].fnDraw();
}

function cbb_logger_type_change() {
  var logger_type = $("#cbbTypeLogger").val();
  $r_id = $("#r-id");
  $r_title = $("#r-title");
  $r_ip = $("#r-ip");
  $r_usr = $("#r-usr-pwd");
  $r_ch = $("#r-ch-slot");
  $r_content = $("#r-content");
  $("#rp-content").show();
  if (logger_type === "D_LOGGER") {
    $r_id.show();
    $r_title.show();
    $r_ip.hide();
    $r_usr.hide();
    $r_content.show();
    $r_ch.hide();
  } else if (["INVENTIA", "ADAM", "BL"].includes(logger_type)) {
    $r_id.hide();
    $r_title.show();
    $r_ip.show();
    $r_usr.show();
    $("#d-usr").prop("disabled", logger_type === "ADAM");
    if (logger_type === "ADAM") {
      $("#d-usr-req").html("");
    } else {
      $("#d-usr-req").html("*");
    }
    if (logger_type === "INVENTIA") {
      $r_ch.hide();
      $r_content.show();
    } else {
      $r_ch.show();
      $r_content.hide();
    }
  } else {
    $("#rp-content").hide();
  }
}

function switch_transfer_type() {
  let transfer_type = $("#stations_transfer_type").val();
  $(
    "#m-ftp, #m-mqtt, #btnFTP_Connect, #btncheckFTP_SHOW2, #btn-mqtt-check, .m-client-id"
  ).hide();
  switch (transfer_type) {
    case "mqtt":
      $("#m-mqtt, #btn-mqtt-check, .m-client-id").show();
      break;
    case "ftp":
      $("#m-ftp, #btnFTP_Connect, #btncheckFTP_SHOW2").show();
      break;
    default:
      $("#m-ftp, #btnFTP_Connect, #btncheckFTP_SHOW2").show();
      break;
  }
}

function check_connect_mqtt(options) {
  var defaults = { url: "", data: {} };
  $.extend(defaults, options);
  $.ajax({
    type: "GET",
    dataType: "json",
    url: defaults.url,
    data: defaults.data,
    success: function (data) {
      if (data.success) toastr["success"]("Kết nối thành công!");
      else toastr["warning"]("Kết nối không thành công!");
    },
    error: function (err) {
      toastr["warning"]("Kết nối không thành công!");
    },
  });
}

function tesst() {
  var port = $("#mq-port").val();
  var ws = $("#mq-ws").val();
  var client_id = $("input#stations_mqtt_usr").val();
  console.log(ws, port, client_id);
  var mqtt = new Messaging.Client(ws, parseInt(port, 10), client_id);
  mqtt.onMessageArrived = function onMessageArrived(message) {
    mqtt.disconnect();
    app.showPopup({ content: message.payloadString, title: "Connected" });
  };
  if (mqtt) {
    mqtt.connect({
      timeout: 5,
      keepAliveInterval: 60,
      cleanSession: true,
      useSSL: false,
      onSuccess: function () {
        mqtt.subscribe(client_id);
        toastr["success"]("Kết nối thành công!");
        mqtt.disconnect();
      },
      onFailure: function () {
        toastr["warning"]("Kết nối không thành công!");
      },
    });
  }
}
