$('#slider2').bxSlider({
  mode: 'fade',
  auto: true,
  speed: 1500,
  autoControls: false,
  pager:true,
  controls: true,
  pause: 4000
});

$(document).on('click', function(event){
	var container = $("#nav-main");
	var container2 = $("#menu_mobile");
	if ($(window).width() < 1000)
	{
		if (!container.is(event.target) && container.has(event.target).length === 0 && !container2.is(event.target) && container2.has(event.target).length === 0)
		{
			 $("#nav-main").slideUp();
			 $('#menu_mobile img').attr('src','images/icon-menu.svg');
		}
	}
});

(function($){
	$(window).on("load",function(){
		
		$(".scrollbox").mCustomScrollbar({
			scrollButtons:{enable:false},
			theme:"light-thick",
			scrollbarPosition:"outside",
			mouseWheel: {
			  scrollAmount: 100
			}
		});
	});
})(jQuery);

$('#slider-events').owlCarousel({
	loop:true,
	margin:20,
	dots:false,
	responsiveClass:true,
	nav:true,
	responsive:{
		0:{
			items:1
		},
		540:{
			items:2
		},
		680:{
			items:2
		},
		992:{
			items:3
		},
		1200:{
			items:4
		}
	}
});
$('#slider-tieudiem').owlCarousel({
	loop:true,
	margin:20,
	dots:false,
	responsiveClass:true,
	nav:true,
	items: 1
});
$('#slider-gallery').owlCarousel({
	loop:true,
	margin:20,
	dots:false,
	responsiveClass:true,
	nav:true,
	items: 1
});
$('#slider-video').owlCarousel({
	loop:true,
	margin:20,
	dots:false,
	responsiveClass:true,
	nav:true,
	items: 1
});
$('#slider-human').owlCarousel({
	loop:true,
	margin:20,
	dots:false,
	responsiveClass:true,
	nav:true,
	responsive:{
		0:{
			items:1
		},
		350:{
			items:1
		},
		500:{
			items:2
		},
		992:{
			items:3
		},
		1200:{
			items:4
		}
	}
});
$('#slider-link').owlCarousel({
	loop:true,
	margin:10,
	dots:false,
	responsiveClass:true,
	nav:true,
	responsive:{
		0:{
			items:1
		},
		450:{
			items:2
		},
		680:{
			items:3
		},
		992:{
			items:4
		},
		1200:{
			items:4
		}
	}
});

$(document).ready(function(){
	$('#menu_mobile').click(function () {
		if ($('#nav-main').css('display') == "block")
		{
			$('#menu_mobile img').attr('src','images/icon-menu.svg');
			$('#nav-main').slideUp();
		}
		else{
			$('#menu_mobile img').attr('src','images/close.png');
			$('#nav-main').slideDown();
		}
	});
	$(".selects1").select2({
	  allowClear:true,
	  placeholder: 'Chọn tỉnh'
	});
	$(".selects2").select2({
	  allowClear:true,
	  placeholder: 'Chọn vùng'
	});
	$(".selects3").select2({
	  allowClear:true,
	  placeholder: 'Chọn trạm'
	});
	$(".selects4").select2({
	  allowClear:true,
	  placeholder: 'Chọn ngày'
	});
	$(".selects5").select2({
	  allowClear:true,
	  placeholder: 'Chọn ngày'
	});
	$('input[name="dates"]').daterangepicker({
		locale: {
	        format: 'DD/MM/YYYY'
	    }
	});

	$('.body-tr').click(function(){
		$('.body-tr').removeClass('active');
		$(this).addClass('active');
		var text_name = $(this).find('.width40').find('.text-black').text();
		$('#name_tram').html(text_name);
	});
	if ($('.fancybox-thumb').length > 0)
	{
		lc_lightbox('.fancybox-thumb', {
			wrap_class: 'lcl_fade_oc',
			gallery : true,	
			thumb_attr: 'data-lcl-thumb', 
			
			skin: 'minimal',
			radius: 0,
			padding	: 0,
			border_w: 0,
		});
	}	
	$('.close-ads').click(function(e){
		$(this).parents('.ads-main').hide();
	});
	// $('a.lang').click(function(){
	// 	if ($('.list-lang').css("display") == "none")
	// 	{
	// 		$('.list-lang').slideDown();
	// 	}
	// 	else
	// 	{
	// 		$('.list-lang').slideUp();
	// 	}
	// });
});

$(window).scroll(function(){
	//menu left
	var menu_leff = $('#title_news_offset').offset().top;
	var height_filter = $('.main-filter').height();
	var height_main = $('#title_news_offset').height();
	var total_height = menu_leff + height_main - height_filter;
	var top_screen = $('html, body').scrollTop();
	
	if (top_screen <= menu_leff)
	{
		$('.main-filter').removeClass('fixed');
	}
	if (top_screen > menu_leff)
	{
		$('.main-filter').addClass('fixed');
	}
	if (top_screen > total_height)
	{
		$('.main-filter').removeClass('fixed');
	}

	//quang cao
	var menu_leff2 = $('#ads_right').offset().top;
	var top_offset = $('#title_news_offset').offset().top;
	var height_filter2 = $('.ads-right').height();
	var height_main2 = $('#title_news_offset').height();
	var total_height2 = top_offset + height_main2 - height_filter2;

	if (top_screen <= menu_leff2)
	{
		$('.ads-right').removeClass('fixed');
	}
	if (top_screen > menu_leff2)
	{
		$('.ads-right').addClass('fixed');
	}
	
	if (top_screen > total_height2)
	{
		$('.ads-right').removeClass('fixed');
	}

	//menu top
	if ($(window).width() > 992)
	{
		var menu_top = $('#box_menu').offset().top;
		if (top_screen >= menu_top)
		{
			$('.box-menu').addClass('fixed');
		}
		else
		{
			$('.box-menu').removeClass('fixed');
		}
	}
}).scroll();

$(function(){
	var $banner = $('.banners'), $window = $(window);
	var $topDefault = -20; parseFloat( $banner.css('top'), 10 );
	$window.on('scroll', function(){
		var $top = $(this).scrollTop();
		$banner.stop().animate( { top: ( $top - $topDefault) }, 1000, 'easeOutBack' );
	});

	var $wiBanner = $banner.outerWidth() * 2;
	zindex($('#wrapper').outerWidth());
	$window.on('resize', function(){
		zindex($('#wrapper').outerWidth());
	});
	function zindex(maxWidth){
		if( $window.width() <= maxWidth + $wiBanner ) {
			$banner.addClass('zindex');
		}else{
			$banner.removeClass('zindex');
		}
	}
});