var ZSlider = {
    auto: true,
    init: function () {
        var curImage = 0;
        var totalItem = $(".slide > a").length;
        //auto
        setInterval(function () {
            if (ZSlider.auto && $('#_bannernext').length) {
                if (curImage < totalItem - 1) {
                    ZSlider.next(curImage, totalItem);
                    curImage = curImage + 1;
                } else {
                    ZSlider.next(curImage, totalItem);
                    curImage = 0;
                }
            }
        }, 3000);
        //khi click
        $('#_bannernext').click(function (event) {
            if (curImage < totalItem - 1) {
                ZSlider.next(curImage, totalItem);
                curImage = curImage + 1;
            } else {
                ZSlider.next(curImage, totalItem);
                curImage = 0;
            }
        });
        $('#_bannerprev').click(function (event) {
            if (curImage > 0) {
                ZSlider.prev(curImage, totalItem);
                curImage = curImage - 1;
            } else {
                ZSlider.prev(curImage, totalItem);
                curImage = totalItem - 1;
            }
        });
    },
    fade: function (curImg, nextImg) {
        var c = $("#_fade" + curImg);
        var n = $("#_fade" + nextImg);
        c.fadeOut(100, function () {
            n.fadeIn(200, function () {
            });
        });
    },
    next: function (curImage, totalItem) {
        var nextImg = curImage + 1;
        if (nextImg == totalItem) {
            nextImg = 0;
        }
        if (nextImg < totalItem) {
            ZSlider.fade(curImage, nextImg);
        }
    },
    prev: function (curImage, totalItem) {
        var prevImg = curImage - 1;
        if (curImage == 0) {
            prevImg = totalItem - 1;
        }
        if (prevImg >= 0) {
            ZSlider.fade(curImage, prevImg);
        }
    },
};
var HomeBanner = {
    auto: true,
    animating: false,
    init: function () {
        var curImage = 0;
        var totalItem = $('._nav_fade').length;
        //auto
        setInterval(function () {
            if (HomeBanner.auto && $('#_banner_next').length) {
                if (curImage < totalItem - 1) {
                    HomeBanner.next(curImage, totalItem);
                    curImage = curImage + 1;
                } else {
                    HomeBanner.next(curImage, totalItem);
                    curImage = 0;
                }
            }
        }, 3000);
        //khi click
        $('._nav_fade').click(function (event) {
            if (!HomeBanner.animating) {
                HomeBanner.auto = false;
                $('._nav_fade').removeClass("active");
                var tar = $(this);
                if (tar.prop('tagName') != 'A') {
                    tar = tar.parent('a');
                }
                tar.addClass("active");
                var index = parseInt(tar.attr("rel"), 10);
                if (curImage != index) {
                    HomeBanner.fade(curImage, index);
                    curImage = index;
                }
            }
            return false;
        });
        $('#_banner_next').click(function (event) {
            if (!HomeBanner.animating) {
                HomeBanner.auto = false;
                if (curImage < totalItem - 1) {
                    HomeBanner.next(curImage, totalItem);
                    curImage = curImage + 1;
                } else {
                    HomeBanner.next(curImage, totalItem);
                    curImage = 0;
                }
            }
            return false;
        });
        $('#_banner_prev').click(function (event) {
            if (!HomeBanner.animating) {
                HomeBanner.auto = false;
                if (curImage > 0) {
                    HomeBanner.prev(curImage, totalItem);
                    curImage = curImage - 1;
                } else {
                    HomeBanner.prev(curImage, totalItem);
                    curImage = totalItem - 1;
                }
            }
            return false;
        });
    },
    fade: function (curImg, nextImg) {
        HomeBanner.animating = true;
        var timestamp = new Date().getTime();
        var cur = $("#_fade_" + curImg);
        var nxt = $("#_fade_" + nextImg);
        var trackingImpress = cur.attr("trackingImpress");
        var zTrackingImpress = cur.attr("zingTrackingImpress");
        if (trackingImpress && trackingImpress != "") {
            cur.append("<img width=0 heigh=0 style='position:absolute;top:9999;' src='" + trackingImpress.replace('[timestamp]', timestamp) + "' />");
        }
        if (zTrackingImpress && zTrackingImpress != "") {
            cur.append("<img width=0 heigh=0 style='position:absolute;top:9999;' src='" + zTrackingImpress.replace('[timestamp]', timestamp) + "' />");
        }

        cur.fadeOut(250, function () {
            nxt.fadeIn(250, function () {
                HomeBanner.animating = false;
            });
        });
    },
    next: function (curImage, totalItem) {
        var nextImg = curImage + 1;
        var o = $('._nav_fade');
        if (nextImg == totalItem) {
            nextImg = 0;
        }
        if (nextImg < totalItem) {
            o.removeClass("active");
            for (var i = 0; i < o.length; i++) {
                var el = $(o[i]);
                var index = parseInt(el.attr("rel"), 10);
                if (index == nextImg) {
                    el.addClass("active");
                }
                ;
            }
            ;
            HomeBanner.fade(curImage, nextImg);
        }
    },
    prev: function (curImage, totalItem) {
        var prevImg = curImage - 1;
        var o = $('._nav_fade');
        if (curImage == 0) {
            prevImg = totalItem - 1;
        }
        if (prevImg >= 0) {
            o.removeClass("active");
            for (var i = 0; i < o.length; i++) {
                var el = $(o[i]);
                var index = parseInt(el.attr("rel"), 10);
                if (index == prevImg) {
                    el.addClass("active");
                }
                ;
            }
            HomeBanner.fade(curImage, prevImg);
        }
    },
};
var CommonScreen = {
    itemPerPage: 6,
    pageWidth: 0,
    windowWidth: 0,
    /**
     * <1024 --> 718:3
     * 1024-<1255 --> 960:4
     * 1255-<1500 --> 1206:5
     * >=1500--> 1451:6
     */
    getScreenProperties: function () {
        var wWidth = $(window).width();
        $(window).resize(function () {
            wWidth = $(window).width();
        });
        var pageWidth = 1451;
        if (wWidth < 1006) {
            pageWidth = 718;
        } else if (wWidth < 1255) {
            pageWidth = 960;
        } else if (wWidth < 1500) {
            pageWidth = 1206;
        }
        pageWidth = pageWidth + 20
        //item perpage tren 1 hang(gia dinh la 1x1)
        var itemPerPage = 6;
        if (wWidth < 1006) {
            itemPerPage = 3;
        } else if (wWidth < 1255) {
            itemPerPage = 4;
        } else if (wWidth < 1500) {
            itemPerPage = 5;
        }
        return {
            itemPerPage: itemPerPage,
            pageWidth: pageWidth,
            windowWidth: wWidth,
            maxItem: 6
        };
    },
    getPageWidth: function () {
        var screenProperties = CommonScreen.getScreenProperties();
        return screenProperties.pageWidth;
    },
    init: function () {
        var screenProperties = CommonScreen.getScreenProperties();
        CommonScreen.itemPerPage = screenProperties.itemPerPage;
        CommonScreen.pageWidth = screenProperties.pageWidth;
        CommonScreen.windowWidth = screenProperties.windowWidth;
    }
}
var HomeSlider = {
    idPrefix: '_page_',
    clickable: true,
    /**
     * lay so item thuc te cua tung loai box
     * @param {int} boxType: 0 => page 1x1, 1=>page 2x1 (item dau=4:2x2)
     * 2 => page 1x1 (item dau=2:1x2)
     * @returns {undefined}
     */
    getPageItem: function (pageObj, isFirstPage) {
        var screenProperties = CommonScreen.getScreenProperties();
        var itemPerPage = screenProperties.itemPerPage;
        if (!isFirstPage)
            isFirstPage = false;
        var items = 0;
        var boxType = typeof (pageObj.attr("boxtype")) != 'undefined' ? parseInt(pageObj.attr("boxtype"), 10) : 0;

        switch (boxType) {
            case 1:
                items = isFirstPage ? (itemPerPage * 2 - 3) : itemPerPage * 2;
                break;
            case 2:
                items = isFirstPage ? (itemPerPage - 1) : itemPerPage;
                break;
            default:
                items = itemPerPage;
        }
        return items;
    },
    getItemChange: function (delta, boxType) {
        var items = 0;
        switch (boxType) {
            case 1:
                items = delta * 2;
                break;
            case 2:
                items = delta;
                break;
            default:
                items = delta;
        }
        return items;
    },
    getImageOnScreen: function (pageObj, isFirstPage) { //chi lay nhung image hien tren man hinh
        if (!isFirstPage)
            isFirstPage = false;
        var index = 0;
        var onsCreenImage = []; //nhung image hien ra man hinh
        var imageChildren = pageObj.find("._slideimg");
        var itemOnPage = HomeSlider.getPageItem(pageObj, isFirstPage);
        imageChildren.each(function () {
            var o2 = $(this);
            var leftPosition = Math.round(o2.position().left);
            //var leftPosition = Math.round(o2.offset().left);
            if (leftPosition >= 0 && index < itemOnPage) {
                index++;
                onsCreenImage.push(o2);
            }
        });
        var firstImage = $(imageChildren[0]); //image dau cua slide
        var lastImage = $(imageChildren[imageChildren.length - 1]); //image cuoi cung cua slide
        var firstBoundImage = onsCreenImage[0]; //image dau nam trong man hinh
        var lastBoundImage = onsCreenImage[onsCreenImage.length - 1]; //image cuoi cung nam trong man hinh
        return {
            firstImage: firstImage,
            lastImage: lastImage,
            onScreenImage: onsCreenImage,
            firstBoundImage: firstBoundImage,
            lastBoundImage: lastBoundImage
        };
    },
    getItemOnOnceRow: function (pageObj) {
        var items = 0;
        var boxType = typeof (pageObj.attr("boxtype")) != 'undefined' ? parseInt(pageObj.attr("boxtype"), 10) : 0;
        var lastImage = typeof (pageObj.attr("lastImage")) != 'undefined' ? parseInt(pageObj.attr("lastImage"), 10) : 0;
        switch (boxType) {
            case 1:
                items = Math.round((lastImage + 4) / 2)
                break;
            case 2:
                items = lastImage + 2;
                break;
            default:
                items = lastImage + 1;
        }
        return items;
    },
    slide: function (boxId, isNext) {
        if (HomeSlider.clickable) {
            HomeSlider.clickable = false;
            var o = $('#' + HomeSlider.idPrefix + boxId);
            var imageChildren = o.find("._slideimg");
            var children = o.find(".subtray");
            var screenProperties = CommonScreen.getScreenProperties();
            var itemPerPage = screenProperties.itemPerPage;
            var itemWidth = children[1] ? $(children[1]).width() : $(children[0]).width();
            var pageWidth = itemWidth * itemPerPage; //CommonScreen.getPageWidth();
            var p2 = 0;
            var temp1 = $("#" + HomeSlider.idPrefix + boxId).css("margin-left");
            var p1 = parseInt(temp1, 10);
            var itemOnPage = HomeSlider.getPageItem(o);
            var itemOnFirstPage = HomeSlider.getPageItem(o, true);
            var itemOnOnceRow = HomeSlider.getItemOnOnceRow(o);
            //p2 = p1 - pageWidth;
            var lastImage = parseInt(o.attr("lastImage"), 10);
            var newLastImage = 0;
            if (isNext) {
                p2 = p1 - pageWidth;
                for (var i = lastImage + 1; i <= itemOnPage + lastImage; i++) {
                    if (imageChildren[i]) {
                        if (newLastImage < i) {
                            newLastImage = i;
                        }
                        var image = $(imageChildren[i]);
                        if (image) {
                            var originalImage = image.attr("_src");
                            var currentImage = image.attr("src");
                            if (originalImage && originalImage != currentImage) {
                                image.attr("src", originalImage);
                            }
                        }
                    }
                }
            } else {
                newLastImage = lastImage - itemOnPage;
                if (newLastImage < itemOnFirstPage) {
                    newLastImage = itemOnFirstPage - 1;
                }
                p2 = p1 + pageWidth;
            }
            var totalLength = 0;
            children.each(function () {
                totalLength += parseInt($(this).width());
            });
            if (newLastImage < 0) {
                newLastImage = 0;
            }
            o.attr('lastImage', newLastImage);
            var idArr = (o.attr("id")).split("_");
            var id = idArr[2];
            if (p2 > 0)
                p2 = 0;
            if (itemOnOnceRow * itemWidth + pageWidth > totalLength && isNext) {
                p2 = -totalLength + pageWidth;
            }
            if (p2 == 0) {
                $("#prev_" + id).addClass("none");
            } else {
                $("#prev_" + id).removeClass("none");
            }
            if (imageChildren[newLastImage + 1]) {
                $("#next_" + id).removeClass("none");
            } else {
                $("#next_" + id).addClass("none");
            }
            $('#' + HomeSlider.idPrefix + boxId).slide({
                duration: 200,
                direction: true,
                start: p1,
                reverse: false,
                end: p2,
                callback: function () {
                    HomeSlider.clickable = true;
                }
            });
        }
    },
    next: function (boxId) {
        HomeSlider.slide(boxId, true);
    },
    prev: function (boxId) {
        HomeSlider.slide(boxId, false);
    },
    parseId: function (id) {
        var idArr = id.split("_");
        return idArr[1];
    },
    initCharts: function (o) {
        var imageOnScreen = HomeSlider.getImageOnScreen(o, true);
        o.attr('lastImage', parseInt(imageOnScreen.lastBoundImage.attr("img_index"), 10));
        for (var i = 0; i < imageOnScreen.onScreenImage.length; i++) {
            var image = imageOnScreen.onScreenImage[i];
            if (image) {
                var originalImage = image.attr("_src");
                var currentImage = image.attr("src");
                if (originalImage && originalImage != currentImage) {
                    image.attr("src", originalImage);
                }
            }
        }
    },
    init: function () {
        var el = $('._page');
        for (var ii = 0; ii < el.length; ii++) {
            var o = $(el[ii]);
            var imageOnScreen = HomeSlider.getImageOnScreen(o, true);
            for (var i = 0; i < imageOnScreen.onScreenImage.length; i++) {
                var image = imageOnScreen.onScreenImage[i];
                if (image) {
                    var originalImage = image.attr("_src");
                    var currentImage = image.attr("src");
                    if (originalImage && originalImage != currentImage) {
                        image.attr("src", originalImage);
                    }
                }
            }
            var idArr = (o.attr("id")).split("_");
            var id = idArr[2];
            if (imageOnScreen.firstImage.offset().left <= imageOnScreen.firstBoundImage.offset().left) {
                $("#prev_" + id).addClass("none");
            } else {
                $("#prev_" + id).removeClass("none");
            }
            if (imageOnScreen.lastImage.offset().left > imageOnScreen.lastBoundImage.offset().left) {
                $("#next_" + id).removeClass("none");
            } else {
                $("#next_" + id).addClass("none");
            }
            o.attr('lastImage', parseInt(imageOnScreen.lastBoundImage.attr("img_index"), 10));
        }
        ;
    },
    resize: function () {
        var oldItemPerPage = CommonScreen.itemPerPage
        var currentScreenProperties = CommonScreen.getScreenProperties();
        var currentItemPerPage = currentScreenProperties.itemPerPage;
        var delta = currentItemPerPage - oldItemPerPage;
        var el = $("._page");
        for (var i = 0; i < el.length; i++) {
            var pageObj = $(el[i]);
            var boxType = typeof (pageObj.attr("boxtype")) != 'undefined' ? parseInt(pageObj.attr("boxtype"), 10) : 0;
            var total = typeof (pageObj.attr("total")) != 'undefined' ? parseInt(pageObj.attr("total"), 10) : 0;
            var itemChange = HomeSlider.getItemChange(delta, boxType);
            var itemOnPage = HomeSlider.getItemChange(currentItemPerPage, boxType);
            var lastImage = parseInt(pageObj.attr("lastImage"), 10);
            var newLastImage = lastImage + itemChange;
            if (newLastImage < 0) {
                newLastImage = 0;
            }
            pageObj.attr('lastImage', newLastImage);
            var imageChildren = pageObj.find("._slideimg");
            if (delta > 0) {
                for (var i = lastImage; i <= newLastImage; i++) {
                    var image = $(imageChildren[i]);
                    if (image) {
                        var originalImage = image.attr("_src");
                        var currentImage = image.attr("src");
                        if (originalImage && originalImage != currentImage) {
                            image.attr("src", originalImage);
                        }
                    }
                }

            }
            var idArr = (pageObj.attr("id")).split("_");
            var id = idArr[2];
            var leftPos = $(imageChildren[0]).offset().left;
            if (leftPos > 0) {
                $("#prev_" + id).addClass("none");
            } else {
                $("#prev_" + id).removeClass("none");
            }
            if (imageChildren[newLastImage + 1]) {
                $("#next_" + id).removeClass("none");
            } else {
                $("#next_" + id).addClass("none");
            }
        }
        ;
    }
};
var Footer = {
    clickable: true,
    init: function () {
        var o = $('#_footer_partner');
        var children = o.find("li");
        var totalLength = 0;
        for (var i = 0; i < children.length; i++) {
            totalLength += parseInt($(children[i]).width(), 10);
        }
        var next = true;
        var pageWidth = CommonScreen.getPageWidth();
        if (totalLength <= pageWidth) {
            /*$("#_footer_partner_next").addClass("none");*/
            
        } else {
            $("#_footer_partner_next").removeClass("none");
        }
        
        /*var priority = 'next';      
        setInterval(function () {
            if(priority == 'next'){
                if ($('#_footer_partner_next').css('display') == 'block'){
                    $('#_footer_partner_next').click();
                    priority = 'next'; 
                }
                else if($('#_footer_partner_prev').css('display') == 'block'){
                    $('#_footer_partner_prev').click();
                    priority = 'prev';                    
                }
            }
            else if(priority == 'prev'){
                if($('#_footer_partner_prev').css('display') == 'block'){
                    $('#_footer_partner_prev').click();
                    priority = 'prev';
                }
                else if ($('#_footer_partner_next').css('display') == 'block'){
                    $('#_footer_partner_next').click();
                    priority = 'next'; 
                } 
            }
            
        }, 3000);*/
    },
    slide: function (isNext) {
        if (Footer.clickable) {
            Footer.clickable = false;
            var o = $('#_footer_partner');
            var children = o.find("li");
            var totalLength = 0;
            for (var i = 0; i < children.length; i++) {
                totalLength += parseInt($(children[i]).width());
            }
            ;

            var pageWidth = CommonScreen.getPageWidth();
            var p2 = 0;

            var temp1 = $("#_footer_partner").css("margin-left");
            var p1 = parseInt(temp1, 10);

            p2 = p1 - pageWidth;
            var curPage = typeof (o.attr("page")) != 'undefined' ? parseInt(o.attr("page"), 10) : 1;
            if (isNext) {
                o.attr("page", curPage + 1);
                p2 = p1 - pageWidth;
            } else {
                o.attr("page", curPage - 1);
                p2 = p1 + pageWidth;
            }
            var curPage = typeof (o.attr("page")) != 'undefined' ? parseInt(o.attr("page"), 10) : 1;
            if (curPage * pageWidth >= totalLength) { //disable next button
                $("#_footer_partner_next").addClass("none");
            } else {
                $("#_footer_partner_next").removeClass("none");
            }
            if (curPage <= 1) { ////disable prev button
                $("#_footer_partner_prev").addClass("none");
            } else {
                $("#_footer_partner_prev").removeClass("none");
            }
            if (p2 > 0)
                p2 = 0;
            $('#_footer_partner').slide({
                duration: 300,
                direction: true,
                start: p1,
                reverse: false,
                end: p2,
                callback: function () {
                    Footer.clickable = true;
                }
            });
        }
    }
};
var Artist = {
    init: function () {
        if ($('._artistdata').length) {
            var elementLink = new Array();
            var elementProfile = new Array();
            var elementSameProfile = new Array();
            var o = $('._artistdata');
            for (var i = 0; i < o.length; i++) {
                var el = $(o[i]);
                var id = el.attr("id");
                var type = el.attr("type");
                if (type == 'profile') {
                    elementProfile.push(id);
                }
                if (type == 'same_profile') {
                    elementSameProfile.push(id);
                }
                if (type == 'link') {
                    if(id != ""){
                        elementLink.push(id);
                    }                    
                }
            }
            ;
            Artist.loadArtist('link', elementLink);
            Artist.loadArtist('profile', elementProfile);
            Artist.loadArtist('same_profile', elementSameProfile);
        }
    },
    loadArtist: function (objectType, objectIdArr) {        
        if (objectIdArr.length > 0) {
            var objectIds = objectIdArr.join(",");
            $.getJSON("/xhr/artist/get-artist" + "?type=" + objectType + "&id=" + objectIds, function (obj) { 
                switch(objectType){
                    case "link":
                        for (var i = 0; i < obj.length; i++) {
                            var object = obj[i];
                            var domObj = $('#' + object.id);
                            if (object.html)
                                domObj.html(object.html);
                            }
                    break;
                    default:
                        var domObj = $('#' + obj.id);
                        if (obj.html){
                            domObj.html(obj.html);
                        }     
                        if ($('._next').size()) {
                            HomeSlider.init();
                            $('._next').click(function (event) {
                                var id = $(this).attr("id");
                                var boxId = HomeSlider.parseId(id);
                                HomeSlider.next(boxId);
                                return false;
                            });
                            $('._prev').click(function (event) {
                                var id = $(this).attr("id");
                                var boxId = HomeSlider.parseId(id);
                                HomeSlider.prev(boxId);
                                return false;
                            });
                        }     
                    break;
                }                 
            });
        }
    }
};

                 

var Subcribe = {
    init: function () {
        Subcribe.loadSubs();
        var o = $('._subscription');       
        $(o).click(function (event) {
            if (MP3.USER_NAME == "") {
                return Login.show(function () {
                });
            } else {
                var _this = $(this);//o;
                var id = _this.attr('pid');
                var type = _this.attr('type');
                $.ajax({
                    url: "/xhr/subcribe/set-subcribe?id=" + id + "&type=" + type,
                    jsonp: "callback",
                    dataType: "jsonp",
                    success: function (obj) {
                        if (obj.error == 0) {
                            if (obj.isSubs) {
                                _this.addClass('subcribed');
                            } else {
                                _this.removeClass('subcribed');
                            }
                            var totalSubsField = $("._total_subs_user");
                            if (totalSubsField.length) {
                                var total = obj.total;
                                if(total >= 0){
                                    if (total > 1000) {
                                        total = Math.round(total / 1000 - 0.5) + 'k';
                                    }
                                    totalSubsField.removeClass("none");
                                    var content = '<i></i><b></b>' + total;
                                    totalSubsField.html(content);
                                }else{
                                    totalSubsField.addClass("none");
                                }
                            }
                            _this.parents("#item_"+id).fadeOut("400", function() {
                                $("#item_"+id).remove();
                            });                            
                        }
                    }
                });
            }
            return false;
        });
    },
    loadSubs: function () {
        var _this = $('._subscription');
        if (_this.size()) {
            var id = _this.attr('pid');
            var type = _this.attr('type');
            $.ajax({
                url: "/xhr/subcribe/get-subcribe?id=" + id + "&type=" + type,
                jsonp: "callback",
                dataType: "jsonp",
                success: function (obj) {
                    if (obj.isSubs) {
                        _this.addClass('subcribed');
                    } else {
                        _this.removeClass('subcribed');
                    }
                    var totalSubsField = $("._total_subs_user");
                    if (totalSubsField.length) {
                        var total = obj.total;
                        if(total >= 0){
                            if (total > 1000) {
                                total = Math.round(total / 1000 - 0.5) + 'k';
                            }
                           totalSubsField.removeClass("none");
                           var content = '<i></i><b></b>' + total;
                            totalSubsField.html(content);
                        }else{
                            totalSubsField.addClass("none");
                        }
                    }
                }
            });
        }
    }
};

var ZingNews = {
    newsBox: null,
    init: function () {
        var _this = $('._znews');
        if (_this.size()) {
            var keywords = _this.attr("keywords");
            ZingNews.newsBox = ZingNews.initNewsBox();
            ZingNews.loadNews(keywords);
        }
    },
    initNewsBox: function () {
        return $("<div/>", {
            class: "section-content non-subtitle fluid"
        }).append($("<div/>", {
            class: "title-bar group",
            html: "<h3>Tin Tức</h3>"
        }));
    },
    initNewsFeatured: function (obj) {
        var link = $("<a/>", {
            href: obj.link,
            class: "thumb",
            target: "_blank",
            html: '<img width="225" height="" src="' + obj.cover + '" alt="' + obj.title + '" />'
        });
        var featureBx = $("<div/>", {
            class: "news-feature"
        }).append(link).append('<h4><a href="' + obj.link + '" target="_blank">' + obj.title + '</a></h4><p>' + obj.summary + '</p>')
        return featureBx;
    },
    loadNews: function (keywords) {
        if (keywords) {
            $.get(
                    "http://news.zing.vn/api/mobile/search.json?keywords=" + keywords, {
                        'dataType': 'json'
                    },
            function (data) {
                var obj = data.data;
                if (!obj.length) {
                    return;
                }
                ;

                var relatedBox = $("<ul/>");
                for (var i = 1; i < obj.length && i < 5; i++) {
                    relatedBox.append($("<li/>", {
                        html: '<a href="' + obj[i].link + '" target="_blank">' + obj[i].title + '</a>'
                    }));
                }
                var fluid = $("<div/>", {
                    class: "fluid"
                }).append(ZingNews.initNewsFeatured(obj[0])).append(relatedBox);
                $('._znews').append(ZingNews.newsBox.append(fluid));
            });
        }
    }
};


$(document).ready(function () {
    ZSlider.init();
    HomeBanner.init();
    CommonScreen.init();
    HomeSlider.init();
    Subcribe.init();
    ZingNews.init();
    if ($('._next').size()) {
        $(window).resize(function () {
            HomeSlider.resize();
            CommonScreen.init();
        });
    }
    $('._next').click(function (event) {
        var id = $(this).attr("id");
        var boxId = HomeSlider.parseId(id);
        HomeSlider.next(boxId);
        return false;
    });
    $('._prev').click(function (event) {
        var id = $(this).attr("id");
        var boxId = HomeSlider.parseId(id);
        HomeSlider.prev(boxId);
        return false;
    });
    if ($('#_footer_partner_next').size()) {
        Footer.init();
        $(window).resize(function () {
            Footer.init();
        });
    }
    $('#_footer_partner_next').click(function (event) {
        Footer.slide(true);
        return false;
    });
    $('#_footer_partner_prev').click(function (event) {
        Footer.slide(false);
        return false;
    });
    Artist.init();

});