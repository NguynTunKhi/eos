$(document).ready(function() {
    $('#btnSave').click(function(){
        if ($("#start").val() == '') {
            alert("Please choose start date!");
            return false;
        }
        
        app.showConfirmBox({
            content: "Do you want to generate data?",
            callback: function() {
                $("textarea#content").html('Start! \n');
                var url = $("#urlGen").val();
                var start = $('#start').val();
                var end   = $('#end').val();
                
                app.postAjax({
                    url: url,
                    data: { 'start' : start, 'end' : end },
                    callback: function (res) {
                        if (res.success) {
                            $("textarea#content").html('Finished! \n' + res.total + ' records \n' + res.end + ' seconds');
                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });

    $('#btnCreateDataAdjust').click(function(){
        if ($("#start").val() == '') {
            alert("Please choose start date!");
            return false;
        }
        var url = $(this).attr('data-url')
        app.showConfirmBox({
            content: "Do you want to copy adjust data?",
            callback: function() {
                $("textarea#content").html('Start! \n');
                var start = $('#start').val();
                var end   = $('#end').val();
                app.postAjax({
                    url: url,
                    data: { 'start' : start, 'end' : end },
                    callback: function (res) {
                        if (res.success) {
                            $("textarea#content").html('Finished! \n' + res.total + ' records \n' + res.end + ' seconds');
                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });
    
    $('#btnCalc').click(function(){
        if ($("#start").val() == '') {
            alert("Please choose start date!");
            return false;
        }
        
        app.showConfirmBox({
            content: "Do you want to calculate data?",
            callback: function() {
                $("textarea#content").html('Start! \n');
                var url = $("#urlCalc").val();
                var start = $('#start').val();
                var end   = $('#end').val();
                
                app.postAjax({
                    url: url,
                    data: { 'start' : start, 'end' : end },
                    callback: function (res) {
                        if (res.success) {
                            $("textarea#content").html('Finished! \n' + res.end + ' seconds');
                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });
    
    $('#btnThreshold').click(function(){
        app.showConfirmBox({
            content: "Do you want to update thresholds?",
            callback: function() {
                $("textarea#content").html('Start! \n');
                var url = $("#urlThreshold").val();
                
                app.postAjax({
                    url: url,
                    data: { },
                    callback: function (res) {
                        if (res.success) {
                            $("textarea#content").html('Finished! \n');
                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });
    
    $('#btnGetData2').click(function(){
        app.showConfirmBox({
            content: "Do you want to getData2?",
            callback: function() {
                $("textarea#content").html('Start! \n');
                var url = $("#urlGetData2").val(); 
                app.postAjax({
                    url: url,
                    data: { },
                    callback: function (res) {
                        if (res.success) {
                            $("textarea#content").html('Finished! \n');
                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });
    
    $('#btnGetData3').click(function(){
        app.showConfirmBox({
            content: "Do you want to getData3?",
            callback: function() {
                $("textarea#content").html('Start! \n');
                var url = $("#urlGetData3").val();
                
                app.postAjax({
                    url: url,
                    data: { },
                    callback: function (res) {
                        if (res.success) {
                            $("textarea#content").html('Finished! \n');
                        } else {
                            app.showError(res.message);
                        }
                    }
                });
            }
        });
    });
});
