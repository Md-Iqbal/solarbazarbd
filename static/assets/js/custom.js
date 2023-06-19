function toggleCart() {
  var element = document.getElementById('custom_drop_item_id');
  element.classList.toggle('custom_drop_item_class');
}

// Latest Slider
$('.new_slider').slick({
  infinite: true,
  slidesToShow: 5,
  prevArrow:
    '<span class="prev_arrow_latest"><i class="fa fa-chevron-left" aria-hidden="true"></i></span>',
  nextArrow:
    '<span class="next_arrow_latest"><i class="fa fa-chevron-right" aria-hidden="true"></i></span>',
  autoplay: true,
  autoplaySpeed: 2000,
  slidesToScroll: 5,
  responsive: [
    {
      breakpoint: 1024,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 3,
        infinite: true,
      },
    },
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 2,
      },
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      },
    },
    // You can unslick at a given breakpoint now by adding:
    // settings: "unslick"
    // instead of a settings object
  ],
});

// =================================== Hide-Show on scroll .site-header.header-v1 .primary-navigation
$(window).scroll(function () {
  var scrollto = $(window).scrollTop();

  if (scrollto > 100) {
    $('.site-branding').css({ display: 'none' });
    $('.custom_nav').css({
      padding: '20px 0',
      flex: '0 0 100%',
      'max-width': '100%',
    });
  } else {
    $('.site-branding').css({ display: 'block' });
    $('.custom_nav').css({
      padding: '20px 0',
      flex: '0 0 75%',
      'max-width': '75%',
    });
  }
});

// =====================================

var coll = document.getElementsByClassName('mobile_dept');
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener('click', function () {
    this.classList.toggle('mobile_active');
    var content = this.nextElementSibling;
    if (content.style.display === 'block') {
      content.style.display = 'none';
    } else {
      content.style.display = 'block';
    }
  });
}

// =================================== Hide-Show on scroll .site-header.header-v1 .primary-navigation
$(window).scroll(function () {
  var scrollto = $(window).scrollTop();

  if (scrollto > 100) {
    $('.overlay').css({ backgroundColor: 'rgba(0, 0, 0, 0.3)' });
    $('.site-branding').css({ display: 'none' });
    $('.custom_nav').css({
      padding: '5px 0 0 0',
      flex: '0 0 100%',
      'max-width': '100%',
      'color':'#f5363e',
    });
  } else {
    $('.overlay').css({ backgroundColor: 'rgba(0, 0, 0, 0)' });
    $('.site-branding').css({ display: 'block' });
    $('.custom_nav').css({
      padding: '20px 0',
      flex: '0 0 75%',
      'max-width': '75%',
    });
  }
});
