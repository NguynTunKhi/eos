/*	
*	############################################################################
*	
*	Delicate Theme Switcher Script
*	---------------------------------------------------------------------
*	@version	1.1
*	@author		The Develovers
*	@link		http://www.thedevelovers.com
*	@copyright	Copyright 2013 The Develovers
*	---------------------------------------------------------------------
*	
*	Manage layout and texture changes
*
*	############################################################################
*/


jQuery(document).ready(function($) {
    // toggle function
	$.fn.clickToggle = function( f1, f2 ) {
		return this.each( function() {
			var clicked = false;
			$(this).bind('click', function() {
				if(clicked) {
					clicked = false;
					return f2.apply(this, arguments);
				}

				clicked = true;
				return f1.apply(this, arguments);
			});
		});

	}	
    
	// switcher toggle 	
	if( $('body').hasClass('home')){

		$('.del-style-switcher').css('right', '0').delay(1000).animate({
			right: '-=250'
		}, 300);
	
	}else{
	
		$('.del-style-switcher').css('right', '-250px');
	}
		
	$('.del-switcher-toggle').clickToggle(
		function(){
		
			$('.del-style-switcher').animate({
				right: '+=250'
				
			}, 300);
		}, 
		function(){
		
			$('.del-style-switcher').animate({
				right: '-=250'
				
			}, 300);
		}
	);

	// check if skin has already applied before
	var skinLogo = localStorage.getItem('skinLogo');
	var skinLogoDefault = '/vmm/static/images/logo.png';

	if(skinLogo != null) {
		$('.logo img').attr('src', skinLogo);
	}

	// switch items
	$('.switch-skin, .switch-skin-full').click( function(e) {

		e.preventDefault();

		resetStyle();
		$('head').append('<link rel="stylesheet" href="' + $(this).attr('data-skin') + '" type="text/css" />');

		if($(this).hasClass('fullbright')) {
			skinLogo = '/vmm/static/images/logo.png';
		}else {
			skinLogo = skinLogoDefault;
		}

		$('.logo img').attr('src', skinLogo);

		// change logo at invoice page if necessary
		if( ($(this).attr('data-skin') == '/vmm/static/css/skins/transparent.css') && $('.invoice-header img').length > 0 ) {
			$('.invoice-header img').attr('src', '/vmm/static/images/logo.png');
		}
	});

	$('.switch-skin-full').click( function() {
		$('.switch-skin-full').removeClass('selected');
		$(this).addClass('selected');
	});

	// reset stlye
	$('.del-reset-style').click( function() {
		resetStyle();
	});

	function resetStyle() {

		// remove skins and reset logo to default
		$('head link[rel="stylesheet"]').each( function() {

			if( $(this).attr('href').toLowerCase().indexOf("skins") >= 0 )
				$(this).remove();
		});

		$('.logo img').attr('src', '/vmm/static/images/logo.png');

		localStorage.removeItem('skin');
		localStorage.setItem('skinLogo', skinLogoDefault);

		// remove fixed top navigation
		$('.switch-skin-full').removeClass('selected');
	}
	
	
});
