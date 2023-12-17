$(document).ready(function(){
    var url = $("#urlLogo_menu_login").val();
    var data = "";
    app.postAjax({
        url: url,
        data: {},
        callback: function (res) {
            if (res.success) {
                $('#logo_login').html(res.logo_login);
            } else {
                app.showError(res.message);
            }
        }
    });
});