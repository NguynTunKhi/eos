$(document).ready(function() {
    var source = {
        url: $("#calendar").attr("data-url")
    };
    
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: false,
        selectable: true,
        //editable: true,
        selectHelper: true,
        eventSources : [source],
        eventRender: function(event, element) {
            
        },
        eventClick: function(eventObj) {
            var html = "<i> Tạo bởi : " + eventObj.created_by + "</i><br>";
            html += "<i> Ngày tạo : " + eventObj.created_date + "</i><br><br>";
            html += "<p><b>" + eventObj.title + "</b></p><br>";
            html += "<p>" + eventObj.content + "</p>";
            html += "<i class='pull-right'><a href='form/" + eventObj.id + "'> xem thêm >> </a></i><br>";
            html += '<div class="hr-line-dashed"></div>';
            app.showPopup({
                title: '',
                content: html
            });
        },
    });
    

});
