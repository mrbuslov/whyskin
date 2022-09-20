
if ($('.mySwiper')){
    var swiper = new Swiper(".mySwiper", {
        slidesPerView: 4,
        spaceBetween: 20,
        slidesPerGroup: 1,
        loop: true,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        breakpoints: {
            1300: {
                slidesPerView: 4,
            },
            // 1025: {
            //     slidesPerView: 3,
            // },
            700: {
                slidesPerView: 3,
            },
            0: {
                slidesPerView: 2,
                spaceBetween: 5,
            }
        }
    });
}
if($('.mySwiperIndex')){
    $('.mySwiperIndex .swiper-slide').css('display', 'flex'); // для страницы index показываем все слайды, потому что при загрузке они показывались ВСЕ, а не один, пришлось через css скрыть
}

if ($('.mySwiperIndex')){
    var swiper_index = new Swiper(".mySwiperIndex", {
        slidesPerView: 1,
        // spaceBetween: 20,
        // slidesPerGroup: 1,
        loop: true,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        autoplay: {
            delay: 4000,
            pauseOnMouseEnter: true,
            disableOnInteraction: false
        },
        speed: 1500,
    });
}



/* 

<div class="slider">
    <div class="slider-line">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
        <img src="{% static 'img/empty_star.svg' %}" alt="">
    </div>
</div>
<button class="slider-prev">Prev</button>
<button class="slider-next">Next</button>




$( document ).ready(function() {
    var slider_width = $('.slider').width();
    var one_elem_w = slider_width/4;

    $('.slider-line img').each(function(){
        $(this).css('width', one_elem_w);
    })
    var slider_line_w = $('.slider-line').width();
    $('.slider').css('height', one_elem_w);

    let offset = 0;
    const sliderLine = document.querySelector('.slider-line');

    document.querySelector('.slider-next').addEventListener('click', function(){
        offset = offset + one_elem_w;
        if (offset > slider_line_w) {
            offset = 0;
        }
        sliderLine.style.left = -offset + 'px';
    });

    document.querySelector('.slider-prev').addEventListener('click', function () {
        offset = offset - one_elem_w;
        if (offset < 0) {
            offset = slider_line_w;
        }
        sliderLine.style.left = -offset + 'px';
    });
})
*/