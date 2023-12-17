$(document).ready(function(){
    var url = $("#urlLogo_menu").val();
    var data = "";
    app.postAjax({
        url: url,
        data: {},
        callback: function (res) {
            if (res.success) {
                $('#logo').html(res.logo);
            } else {
                app.showError(res.message);
            }
        }
    });
});