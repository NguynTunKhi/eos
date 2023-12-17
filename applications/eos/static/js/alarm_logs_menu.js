
// $(document).ready(function(){
//     var url = $("#urlAlarmLogs_menu").val();
//     var data = "";
//     app.postAjax({
//         url: url,
//         data: {},
//         callback: function (res) {
//             if (res.success) {
//                 $('#alarm_menu').html(res.html_total);
//                 $('#alarm_logs_header').html(res.html);
//                 $('#station_alarm_menu').html(res.html_station_alarm);
//                 $('#station_inactive_menu').html(res.html_station_inactive);
//                 $('#indicator_alarm_menu').html(res.html_indicator_alarm);
//                 $('#not_solve_alarm_menu').html(res.html_not_solve_alarm);
//                 $('#equipment_error').html(res.html_equipment_error);
//             } else {
//                 app.showError(res.message);
//             }
//         }
//     });
// });