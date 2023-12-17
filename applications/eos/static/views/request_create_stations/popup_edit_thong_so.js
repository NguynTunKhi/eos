$(document).ready(function () {
    app.registerEventsForCommonInput();

    $('.chosen-container-single').css('width', '100%');

    const_value = $("#ecbbQCVN_8 option:selected").attr("value_const");
    console.log("const_value",const_value)
    if (const_value == 1) {
      $("#eqcvn_detail_const_area_value_1").attr("type", "number");
      $("#eqcvn_detail_const_area_value_2").attr("type", "number");
      $("#eqcvn_detail_const_area_value_3").attr("type", "number");
      $("#elbl_qcvn_detail_const_area_value_type").attr(
        "style",
        "Display: block;"
      );
      $("#elbl_qcvn_detail_const_area_value_1").attr("style", "Display: block;");
      $("#elbl_qcvn_detail_const_area_value_2").attr("style", "Display: block;");
      $("#elbl_qcvn_detail_const_area_value_3").attr("style", "Display: block;");
    } else {
      $("#eqcvn_detail_const_area_value_1").attr("type", "hidden");
      $("#eqcvn_detail_const_area_value_2").attr("type", "hidden");
      $("#eqcvn_detail_const_area_value_3").attr("type", "hidden");
      $("#elbl_qcvn_detail_const_area_value_type").attr(
        "style",
        "Display: block;"
      );
      $("#elbl_qcvn_detail_const_area_value_1").attr("style", "Display: none;");
      $("#elbl_qcvn_detail_const_area_value_2").attr("style", "Display: none;");
      $("#elbl_qcvn_detail_const_area_value_3").attr("style", "Display: none;");
    }
    var temp = false;
    $("body").on("change", "#ecbbQCVN_8", function (e) {
      $(".validationErrorContainer").attr("style", "Display: none;");
      var const_val = $("#ecbbQCVN_8 option:selected").attr("value_const");
      var qcvn_id = $(this).val();
      var url = $(this).data("url");
      var data = { qcvn_id: qcvn_id, request_create_station_id: $("#hfRequestCreateStationId").val() };
  
      app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
          if (res.success) {
            $("#ecbbQCVN_TYPE_CODE_8")
              .empty()
              .append($('<option value=""></option>').text("-- Chọn loại --"));
            $("#ecbbIndicatorId")
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
              $("#eqcvn_detail_const_area_value_1").attr("type", "hidden");
              $("#eqcvn_detail_const_area_value_2").attr("type", "hidden");
              $("#eqcvn_detail_const_area_value_3").attr("type", "hidden");
              $("#elbl_qcvn_detail_const_area_value_type").attr(
                "style",
                "Display: none;"
              );
              $("#elbl_qcvn_detail_const_area_value_1").attr(
                "style",
                "Display: none;"
              );
              $("#elbl_qcvn_detail_const_area_value_2").attr(
                "style",
                "Display: none;"
              );
              $("#elbl_qcvn_detail_const_area_value_3").attr(
                "style",
                "Display: none;"
              );
              $("#ecbbQCVN_TYPE_CODE_8_chosen").attr("style", "Display: none;");
              $.each(res.indicators, function (key, value) {
                var value_option = value.id;
                var text = value.id != null ? value.indicator : "-";
                $("#ecbbIndicatorId").append(
                  $("<option></option>")
                    .attr("value", value_option.toString())
                    .text(text)
                );
              });
              $("#ecbbIndicatorId").chosen().trigger("chosen:updated");
              $("#ecbbIndicatorId_chosen").attr("style", "Display: block;");
            } else {
              $.each(res.qcvn_details, function (key, value) {
                var value_option = value.id;
                var text = value.qcvn_kind != null ? value.qcvn_kind : "-";
                $("#ecbbQCVN_TYPE_CODE_8").append(
                  $("<option></option>")
                    .attr("value", value_option.toString())
                    .text(text)
                );
              });
  
              $("#ecbbQCVN_TYPE_CODE_8").chosen().trigger("chosen:updated");
              if (const_val == 1) {
                $("#eqcvn_detail_const_area_value_1").attr("type", "number");
                $("#eqcvn_detail_const_area_value_2").attr("type", "number");
                $("#eqcvn_detail_const_area_value_3").attr("type", "number");
                $("#elbl_qcvn_detail_const_area_value_type").attr(
                  "style",
                  "Display: block;"
                );
                $("#elbl_qcvn_detail_const_area_value_1").attr(
                  "style",
                  "Display: block;"
                );
                $("#elbl_qcvn_detail_const_area_value_2").attr(
                  "style",
                  "Display: block;"
                );
                $("#elbl_qcvn_detail_const_area_value_3").attr(
                  "style",
                  "Display: block;"
                );
              } else {
                $("#eqcvn_detail_const_area_value_1").attr("type", "hidden");
                $("#eqcvn_detail_const_area_value_2").attr("type", "hidden");
                $("#eqcvn_detail_const_area_value_3").attr("type", "hidden");
                $("#elbl_qcvn_detail_const_area_value_type").attr(
                  "style",
                  "Display: block;"
                );
                $("#elbl_qcvn_detail_const_area_value_1").attr(
                  "style",
                  "Display: none;"
                );
                $("#elbl_qcvn_detail_const_area_value_2").attr(
                  "style",
                  "Display: none;"
                );
                $("#elbl_qcvn_detail_const_area_value_3").attr(
                  "style",
                  "Display: none;"
                );
              }
  
              $("#ecbbQCVN_TYPE_CODE_8_chosen").attr("style", "Display: block;");

              $.each(res.indicators, function (key, value) {
                var value_option = value.id;
                var text = value.id != null ? value.indicator : "-";
                $("#ecbbIndicatorId").append(
                  $("<option></option>")
                    .attr("value", value_option.toString())
                    .text(text)
                );
              });
              $("#ecbbIndicatorId").chosen().trigger("chosen:updated");
              $("#ecbbIndicatorId_chosen").attr("style", "Display: block;");
            }
          } else {
            app.showError(res.message);
          }
        },
      });
    });

    $("body").on("change", "#ecbbQCVN_TYPE_CODE", function (e) {
        var id = $(this).val();
        $("#eqcvn_detail_min_value").val(1);
        $("#eqcvn_detail_max_value").val(1);
        // $('#qcvn_detail_const_area_value').val('');
        var url = $(this).data("url");
        var data = { id: id };
        app.postAjax({
          url: url,
          data: data,
          callback: function (res) {
            if (res.success) {
              $("#eqcvn_detail_min_value").val(
                Math.ceil(res.qcvn_detail.qcvn_min_value * 1.1 * 1.2)
              );
              $("#eqcvn_detail_max_value").val(
                Math.ceil(res.qcvn_detail.qcvn_max_value * 1.1 * 1.2)
              );
              $("#eqcvn_detail_const_area_value").val(
                res.qcvn_detail.qcvn_const_area_value
              );
            } else {
              app.showError(res.message);
            }
          },
        });
      });
    // Add new Indicator to station
    $("body").on("click", "#ebtnLinkIndicatorToWaterStation", function (e) {
        form_uri = $("#url_form").val()
        var data = {
          indicator_id: $("#ecbbIndicatorId").val(),
          station_indicator_id: $("#station_indicator_id").val(),
          request_create_station_id: $("#hfRequestCreateStationId").val(),
          station_name: $("#hfStationName").val(),
          qcvn_id: $("#ecbbQCVN_8").val(),
          qcvn_kind_id: $("#ecbbQCVN_TYPE_CODE_8").val(),
          qcvn_code: $("#ecbbQCVN_8 option:selected").text(),
          qcvn_detail_type_code: $("#ecbbQCVN_TYPE_CODE_8 option:selected").text(),
          qcvn_detail_const_area_value_1: $(
            "#eqcvn_detail_const_area_value_1"
        ).val(),
        qcvn_detail_const_area_value_2: $(
            "#eqcvn_detail_const_area_value_2"
        ).val(),
        qcvn_detail_const_area_value_3: $(
            "#eqcvn_detail_const_area_value_3"
        ).val(),
        indicator_name_mapping: $("#eindicator_name_mapping").val(),
        };

        console.log("data", data)

        var url = $(this).data("url");
        app.postAjax({
        url: url,
        data: data,
        callback: function (res) {
            if (res.success) {
                $("#edit_thong_so_close").click()
                oTable[1].fnDraw();
            } else {
                app.showError(res.message);
            }
        },
        });
    });
  
    $("body").on("change", "#ecbbIndicatorId", function (e) {
      var indicator_id = $(this).val();
      var qcvn_kind_id = $("#e").val();
      var qcvn_id = $("#ecbbQCVN_AJAX").val();
      var cons_1 = $("#ecbbQCVN_heso_1").val();
      var cons_2 = $("#ecbbQCVN_heso_2").val();
      
      $("#etxtTendency").val("");
      $("#etxtPreparing").val("");
      $("#etxtExceed").val("");
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
            $("#etxtTendency").val(res.tendency_value);
            $("#etxtPreparing").val(res.preparing_value);
            $("#etxtExceed").val(res.exceed_value);
            $("#eindicator_name_mapping").val(res.source_name);
  
            $("#eqcvn_detail_min_value").val(res.qcvn_min_value_indicator);
            $("#eqcvn_detail_max_value").val(res.qcvn_max_value_indicator);
          } else {
            app.showError(res.message);
          }
        },
      });
    });
});

function reloadDatatable() {
    oTable[0].fnDraw();
}
