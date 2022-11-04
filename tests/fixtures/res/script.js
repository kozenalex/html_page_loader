function number_format(number, decimals, dec_point, thousands_sep) {
number = (number + '').replace(/[^0-9+\-Ee.]/g, '');
var n = !isFinite(+number) ? 0 : +number,
prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
s = '',
toFixedFix = function (n, prec) {
 var k = Math.pow(10, prec);
 return '' + Math.round(n * k) / k;
};
// Fix for IE parseFloat(0.55).toFixed(0) = 0;
s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
if (s[0].length > 3) {
s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
}
if ((s[1] || '').length < prec) {
s[1] = s[1] || '';
s[1] += new Array(prec - s[1].length + 1).join('0');
}
return s.join(dec);
}


(function ($) {

if (!$) return;
$.fn.extend({
    fixPNG: function(sizingMethod, forceBG) {
            if (!($.browser.msie)) return this;
            var emptyimg = "/img/transparent_1x1.gif"; //Path to empty 1x1px GIF goes here
            sizingMethod = sizingMethod || "scale"; //sizingMethod, defaults to scale (matches image dimensions)
            this.each(function() {
                    var isImg = (forceBG) ? false : jQuery.nodeName(this, "img"),
                            imgname = (isImg) ? this.src : this.currentStyle.backgroundImage,
                            src = (isImg) ? imgname : imgname.substring(5,imgname.length-2);
                    this.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + src + "', sizingMethod='" + sizingMethod + "')";
                    if (isImg) this.src = emptyimg;
                    else this.style.backgroundImage = "url(" + emptyimg + ")";
            });
            return this;
    }
});
})(jQuery);


$(document).ready(function() {
	
	
	$('.cardsSwitch .switch').live('click', function(){
		if($(this).hasClass('right')) {
			$(this).prev('a').click();
		} else {
			$(this).next('a').click();
		}
	});
	
	
		
//аккордеон
	var textOld;
	$('.accordion dd').live('click', function() {
	
		$('.accordion dd').removeClass('on');
		$('.accordion dt').slideUp('normal');
		if ($(this).prev().is(':hidden') == true) {
			textOld=$(this).find('span').text();
			$(this).addClass('on');
			$(this).prev().slideDown('normal');
			$(this).find('span').text('Свернуть');
		}
		else
		{
			$(this).find('span').text(textOld);
		}
	});
	$('.accordion dd').live('mouseover', function() {
		$(this).addClass('over');
	});
	$('.accordion dd').live('mouseout', function() {
		$(this).removeClass('over');
	});
	
	$('.accordion dt').hide();
	$('.allCard li .imgCart img').fixPNG();
	
	
	// LIGHTBOX
	if($('.lightbox').length > 0) {
		$('body').append('<div class="shadow-ligtbox"/>');	
	}
	$('.lightbox .close').live('click', function() {
		$('.shadow-ligtbox').hide();
		$(this).parent().fadeOut(200);
		return false;
	});
	$('.shadow-ligtbox').live('click', function() {
		$(this).hide();
		$('.lightbox').fadeOut(200);
	});
	
		
});
$(function() {
	$('.btn').mousedown(function() {
		$(this).addClass('active');
	}).bind('mouseup mouseleave', function() {
		$(this).removeClass('active');
	});
});
$(function() {
	$('.citySelect a, .pageTitle .pseudo').click(function() {
		className = $(this).attr('class');
		if(className != 'active'){
			$(this).addClass('active');
		}
		else{
			$(this).removeClass();
		}
	})
});



/*
//Большие подсказки
$(function() {
	$("a[rel=popover]").popover( {
		offset : 10
	}).click(function(e) {
		e.preventDefault()
	})
});
//Мини-подсказки
$(function() {
	$("a[rel=twipsy]").twipsy( {
		live : true
	})
});
//Табы
$(function() {
	$('.tabs').tabs()
})
//Лайтбокс
$(function() {
    $('.galleryImgWrapper a').fancybox();
});
*/
