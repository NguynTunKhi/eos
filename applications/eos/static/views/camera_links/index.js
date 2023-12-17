$(document).ready(function() {
    setTimeout(function(){
    location.reload();
    },60*60*1000)

    jwplayer.key = '4fIW2J0E542IlbXSI7voFoH2De+H51cCFis9FNAhX2VL+3aa';

    // "test" o day la id cua 1 div
    if (false) {
        jwplayer("test").setup({
            // "file": "/uploads/example.mp4",
            // file: "http://27.118.20.209:1935/live/CAMTEST2.stream/playlist.m3u8",
            file: "http://27.118.20.209:1935/CAM/CAMTEST6.stream/playlist.m3u8",
            // "file": "http://localhost:8000/eos/static/img/test.mp4",
            "image": "/uploads/example.jpg",
            "width": "100%",
            "aspectratio": "4:3",
            "autostart": false,
            "controls": true,
            "preload": "metadata",
            "primary": "html5"
        });

        jwplayer("test2").setup({
            // "file": "/uploads/example.mp4",
            // file: "http://27.118.20.209:1935/live/CAMTEST2.stream/playlist.m3u8",
            file: "http://27.118.20.209:1935/CAM/CAMTEST7.stream/playlist.m3u8",
            // "file": "http://localhost:8000/eos/static/img/test.mp4",
            "image": "/uploads/example.jpg",
            "width": "100%",
            "aspectratio": "4:3",
            "autostart": false,
            "controls": true,
            "preload": "metadata",
            "primary": "html5"
        });

        jwplayer("test3").setup({
            // "file": "/uploads/example.mp4",
            // file: "http://27.118.20.209:1935/live/CAMTEST2.stream/playlist.m3u8",
            file: "http://27.118.20.209:1935/CAM/CAMTEST8.stream/playlist.m3u8",
            // "file": "http://localhost:8000/eos/static/img/test.mp4",
            "image": "/uploads/example.jpg",
            "width": "100%",
            "aspectratio": "4:3",
            "autostart": false,
            "controls": true,
            "preload": "metadata",
            "primary": "html5"
        });
    }

    $('body').off('click', '.bg-video');
    $('body').on('click', '.bg-video', function (e) {
        var target_id = $(this).find('.camera_links').attr('id');
        initPlayVideo({target: '#' + target_id});
    });

    $('#aaa').click(function(){
        alert('aaa')
    });

    $('#btn_record').click(function(){
        alert('btn_record')
    });

    $('body').on('click', '.bg-video3', function (e) {
        var modal = document.getElementById("myModal");
        var target_id = $(this).find('.bg-video1').attr('id');
        var modalImg = document.getElementById("img01");
        modal.style.display = "block";
        modalImg.src = this.src;
        var span = document.getElementsByClassName("close")[0];
        span.onclick = function() {
            modal.style.display = "none";
            }
        if (e.keyCode == 27) {
            modal.style.display = "none";
        }

        target_id.onclick = function(){
          modal.style.display = "block";
          modalImg.src = this.src;
          captionText.innerHTML = this.alt;
}


    });

     $('body').on('click', '.bg-video3', function (e) {
        var modal = document.getElementById("myModal");
        var target_id = $(this).find('.bg-video1').attr('id');
        var modalImg = document.getElementById("img01");
        modal.style.display = "block";
        modalImg.src = this.src;
        var span = document.getElementsByClassName("close")[0];
        span.onclick = function() {
            modal.style.display = "none";
            }
        if (e.keyCode == 27) {
            modal.style.display = "none";
        }

        target_id.onclick = function(){
          modal.style.display = "block";
          modalImg.src = this.src;
          captionText.innerHTML = this.alt;
}


    });

    $('body').on('click', '.bg-video2', function (e) {
        var modal = document.getElementById("myModal");
        var target_id = $(this).find('.bg-video2').attr('id');
        var modalImg = document.getElementById("img01");
        modal.style.display = "block";
        modalImg.src = this.title;
        var span = document.getElementsByClassName("close")[0];
        span.onclick = function() {
            modal.style.display = "none";
            }
        if (e.keyCode == 27) {
            modal.style.display = "none";
        }

        target_id.onclick = function(){
          modal.style.display = "block";
          modalImg.src = this.src;
          captionText.innerHTML = this.alt;
}


    });


    $('#station_type').change(function() {
        var url = $(this).data('url');
        app.postAjax({
            url: url,
            data: {filter_value : $(this).val()},

            callback: function (res) {
                if (res.success) {
                    $('#station_id').html(res.html);
                    $('#station_id').trigger("chosen:updated");
                } else {
                    app.showError(res.message);
                }
            }
        });
    });

    $('#btn_search').click(function(){
        // reset page number
        var page = 1;
        $('#video_list').attr('data-page', page);
        getMoreVideo(page);
    });
    $('#btn_search1').click(function(){
        // reset page number
        var page = 1;
        $('#video_list').attr('data-page', page);
        getMoreVideo(page);
    });

    // Thay doi so man hinh tren 1 row
    $('body').on('click', '.btnChangeColumn', function (e) {
        $('.btnChangeColumn').removeClass('active');
        $(this).addClass('active');
        var num_columns = parseInt($(this).html());
        var css = 12 / num_columns;
        $('.ibox-content.videos .item').attr('class', 'item col-sm-' + css);
    });

    // Thay doi so man hinh tren 1 row
    $('body').off('click', '.btnShowMore');
    $('body').on('click', '.btnShowMore', function (e) {
        var page = $('#video_list').attr('data-page');
        getMoreVideo(page);
    });

    $('#btn_search').trigger('click');
});

function getMoreVideo(page) {
    var url = $('#btn_search').data('url');
    app.postAjax({
        url: url,
        data: {
            page: page,
            type : $('#station_type').val(),
            station_id : $('#station_id').val()
        },
        callback: function (res) {
            if (res.success) {
                if (page == 1) {
                    $('#video_list').html(res.html);    // Fill result content,
                } else {
                    $('.btnShowMore').closest('.text-center').remove();
                    $('#video_list').append(res.html);
                }
                // reset 1 row to display 4 item
                $('.btnChangeColumn').removeClass('active');
                $('#btn_4').addClass('active');
                // register event
                // initPlayVideo({target: '.camera_links'});
                // apply next page
                $('#video_list').attr('data-page', res.next_page);

            } else {
                app.showError(res.message);
            }
        }
    });
}

function changeCamera(value) {
   url = "/eos/camera_links/call/json/change?id="+value
   app.postAjax({
        url: url,
        })
}

function showOptions(value){
  var y = 'options_' + value
  var x = document.getElementById(y);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function test(obj){
  console.log(obj[obj.selectedIndex].value); // get value
  console.log(obj[obj.selectedIndex].id); // get
  var value = obj.value;
  var id = obj[obj.selectedIndex].id


  if (id == 1) {
        location = obj.value
  }
  if (id == 0) {
        url = "/eos/camera_links/popup_record_camera?id=159"
        app.postAjax({
        url: url,
        })
  }
}



var elem = document.documentElement;
function openFullscreen() {
  if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }
}

function closeFullscreen() {
  if (document.exitFullscreen) {
  document.exitFullscreen();
  } else if (document.mozCancelFullScreen) {
  document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) {
  document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
  document.msExitFullscreen();
  }
}

