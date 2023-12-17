$(document).ready(function() {
    $('#btn_history').hide();
    $('body').off('click', '.bg-video');
    $('body').on('click', '.bg-video', function (e) {
        var target_id = $(this).find('.camera_links').attr('id');
        initPlayVideo({target: '#' + target_id});
    });

    $('body').on('click', '.bg-video1', function (e) {
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


    $('#btn_history').click(function(){
        // reset page number
        var page = 1;
        $('#video_list').attr('data-page', page);
        getMoreVideo(page);
    });

    $('#btn_history').trigger('click');
});

function getMoreVideo(page) {
    var url = $('#btn_history').data('url');
//    url = "/eos/camera_links/call/json/history?page="+page
    app.postAjax({
        url: url,
        data: {
            page: page,
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

