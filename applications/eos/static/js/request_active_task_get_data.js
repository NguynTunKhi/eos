/**
 * Created by Admin on 22/11/2017.
 */
 $(document).ready(function(){
     app.showConfirmBox({
        content: app.translate("Active task get data?"),
        cancel_text: app.translate('Later'),
        callback: function () {
            var url = $("#urlStartTaskNow").val();
            var data = "";
            $.ajax({
                type: "POST",
                url: url,
                data: data,
                dataType: 'json',
                success: function(){
                    void(0);
                },
                error: function(err){
                    app.showError(err.status + ": " + err.statusText);
                }
            });
        },
        cancel_callback: function () {
            var url = $("#urlStartTaskLater").val();
            var data = "";
            $.ajax({
                type: "POST",
                url: url,
                data: data,
                dataType: 'json',
                success: function(){
                    void(0);
                },
                error: function(err){
                    app.showError(err.status + ": " + err.statusText);
                }
            });
        }
     });
 });