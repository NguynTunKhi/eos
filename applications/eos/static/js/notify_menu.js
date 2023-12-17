
$(document).ready(function(){
    var url = $("#urlNotify_menu").val();
    var data = "";
    app.postAjax({
        url: url,
        data: {},
        callback: function (res) {
            if (res.success) {
                $('#notifications').html(res.html);
            } else {
                app.showError(res.message);
            }
        }
    });
});