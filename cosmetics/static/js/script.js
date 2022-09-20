function getCookie(name) {
    var matches = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}


function notification(){
    $('.notification').css('left', 'calc(100% - 300px)');
    setTimeout(function(){$('.notification').css('left', '100%');}, 5000);
}
if($('.notif_close')){
    $('.notif_close').on('click', function(){
        $('.notification').css('left', '100%');
    })
}




if($('.images_slider_item')){
    $('.images_slider_item').on('click', function(){
        $('#main_image').css('transition', 'none');
        $('.images_slider_item').css('border', '1px solid #D9D9D9');
        $(this).css('border', '1px solid #424242');
        $('#main_image').css('opacity', 0);

        var new_image_src = $(this).find('img').attr('src');
        var new_image_alt = $(this).find('img').attr('alt');
        var new_image_title = $(this).find('img').attr('title');

        setTimeout(function(){
            $('#main_image').css('transition', 'opacity 0.5s ease');
            $('#main_image').css('opacity', 100);
        }, 70);
        $('#main_image').attr('src', new_image_src);
        $('#main_image').attr('alt', new_image_alt);
        $('#main_image').attr('title', new_image_title);
    })
}


if($(".go_to_desc")){
    $(".go_to_desc").click(function() {
        $([document.documentElement, document.body]).animate({
            scrollTop: $(".description_block").offset().top
        }, 800);
    });
}


// ------------------------------------------- Add to cart ----------------------------------------------------------
if($('.item_add_to_cart')){
    $('.item_add_to_cart').on('click', function(){
        prod_slug = $(this).parents('.product_item').find('.item_name').attr('href').split('/')[2];
        $(this).addClass('button_loading');
        var this_obj = $(this);

        $.ajax({
            url: "/cart/",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            method : "post",
            dataType : "json",
            data : {'prod_slug':prod_slug,},
            success: function (response) {
                this_obj.removeClass('button_loading');
                if(response['status'] === 'add'){
                    this_obj.find('img').attr('src', $('#full_add_to_cart_img').val());
                }
                else if (response['status'] === 'remove'){
                    this_obj.find('img').attr('src', $('#empty_add_to_cart_img').val());
                }
                $('.notif_main').text(response['action']);
                $('.notif_goto_cart').attr('href', response['goto_url']);
                notification();
            },
            error: function (response) {
                alert('Error... Try again later.');
                this_obj.removeClass('button_loading');
            }
        });
    })
}


if($('.prod_add_to_cart')){
    $('.prod_add_to_cart').on('click', function(){
        prod_slug = window.location.href.split('/')[4]
        $('.prod_add_to_cart').addClass('button_loading');
        var this_obj = $(this);
        
        $.ajax({
            url: "/cart/",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            method : "post",
            dataType : "json",
            data : {'prod_slug':prod_slug,},
            success: function (response) {
                $('.prod_add_to_cart').removeClass('button_loading');
                $('.prod_add_to_cart').html(response['button_htmlContent']);
                $('.notif_main').text(response['action']);
                $('.notif_goto_cart').attr('href', response['goto_url']);
                notification();
            },
            error: function (response) {
                alert('Error... Try again later.');
                this_obj.removeClass('button_loading');
            }
        });

    })
}


$(document).on("click",".rel_add_to_cart",function(e) {
    e.preventDefault();
    prod_slug = $(this).parents('.swiper-slide').attr('href').split('/')[2];
    // $(this).addClass('button_loading');
    var this_obj = $(this);

    $.ajax({
        url: "/cart/",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        method : "post",
        dataType : "json",
        data : {'prod_slug':prod_slug,},
        success: function (response) {
            // this_obj.removeClass('button_loading');
            if(response['status'] === 'add'){
                this_obj.attr('src', $('#full_add_to_cart_img').val());
            }
            else if (response['status'] === 'remove'){
                this_obj.attr('src', $('#empty_add_to_cart_img').val());
            }
            $('.notif_main').text(response['action']);
            $('.notif_goto_cart').attr('href', response['goto_url']);
            notification();
        },
        error: function (response) {
            alert('Error... Try again later.');
            // this_obj.removeClass('button_loading');
        }
    });
});


// ------------------------------------- cart -------------------------------------------------

function change_quantity(operation, quantity_num){
    if(operation === 'minus'){
        if (quantity_num.val() > 1) {
            quantity_num.val(+quantity_num.val() - 1);
        }
    }
    else{
        quantity_num.val(+quantity_num.val() + 1);
    }

    total_price = 0;
    $('.carted_prod_details').each(function(){
        total_price += $(this).find('.carted_price_num').text() * $(this).find('.quantity_num').val()
    })
    $('.cart_total_price').html(total_price + ' <span>₴</span>')
}

if($(".quantity_arrow-minus") || $(".quantity_arrow-plus")){
    $(".quantity_arrow-minus").on('click', function(e){change_quantity('minus', $(this).parent().find('.quantity_num'));})
    $(".quantity_arrow-plus").on('click', function(e){change_quantity('plus', $(this).parent().find('.quantity_num'));})
}

if($(".quantity_block")){
    $(".quantity_block").on('click', function(e){e.preventDefault();})
}

if($(".carted_remove")){
    $(document).on("click",".carted_remove",function(e) {
        e.preventDefault();
        prod_slug = $(this).parents('.carted').attr('href').split('/')[2];
        $(this).addClass('button_loading');
        var this_obj = $(this);

        $.ajax({
            url: "/cart/",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            method : "post",
            dataType : "json",
            data : {'prod_slug':prod_slug,},
            success: function (response) {
                this_obj.removeClass('button_loading');
                if(response['status'] === 'add'){
                    this_obj.find('img').attr('src', $('#full_add_to_cart_img').val());
                }
                else if (response['status'] === 'remove'){
                    this_obj.find('img').attr('src', $('#empty_add_to_cart_img').val());
                }
                $('.notif_main').text(response['action']);
                $('.notif_goto_cart').attr('href', response['goto_url']);
                notification();
                this_obj.parents('.carted').remove();
                // изменим общую стоимость товаров
                total_price = 0;
                $('.carted_prod_details').each(function(){
                    total_price += $(this).find('.carted_price_num').text() * $(this).find('.quantity_num').val()
                })
                $('.cart_total_price').html(total_price + ' <span>₴</span>')
            },
            error: function (response) {
                alert('Error... Try again later.');
                this_obj.removeClass('button_loading');
            }
        });

    });
}


// ------------------------------------- add to liked -------------------------------------------------
if($('.item_add_to_liked')){
    $('.item_add_to_liked').on('click', function(){
        prod_slug = $(this).parents('.product_item').find('.item_name').attr('href').split('/')[2];
        var this_obj = $(this);
        var this_obj_loading = $(this).find('.loading_when_clicked');
        this_obj_loading.addClass('button_loading');

        $.ajax({
            url: "/liked/",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            method : "post",
            dataType : "json",
            data : {'prod_slug':prod_slug,},
            success: function (response) {
                this_obj_loading.removeClass('button_loading');
                if(response['status'] === 'add'){this_obj.find('img').attr('src', $('#full_add_to_liked_img').val());}
                else if (response['status'] === 'remove'){this_obj.find('img').attr('src', $('#empty_add_to_liked_img').val());}
                $('.notif_main').text(response['action']);
                $('.notif_goto_cart').attr('href', response['goto_url']);
                notification();
            },
            error: function (response) {
                alert('Error... Try again later.');
                this_obj_loading.removeClass('button_loading');
            }
        });

    })
}


if($('.prod_add_to_liked')){
    $('.prod_add_to_liked').on('click', function(){
        prod_slug = window.location.href.split('/')[4]
        $('.prod_add_to_liked').addClass('button_loading');
        var this_obj = $(this);
        
        $.ajax({
            url: "/liked/",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            method : "post",
            dataType : "json",
            data : {'prod_slug':prod_slug,},
            success: function (response) {
                $('.prod_add_to_liked').removeClass('button_loading');
                if(response['status'] === 'add'){this_obj.find('img').attr('src', $('#full_add_to_liked_img').val());}
                else if (response['status'] === 'remove'){this_obj.find('img').attr('src', $('#empty_add_to_liked_img').val());}
                $('.notif_main').text(response['action']);
                $('.notif_goto_cart').attr('href', response['goto_url']);
                notification();
            },
            error: function (response) {
                alert('Error... Try again later.');
                this_obj.removeClass('button_loading');
            }
        });

    })
}



// ----------------------------------------------- REGISTRATION CHECKBOX CHECKED --------------------------------------------------------

if(document.querySelector('.agree_checkbox')){
    document.querySelector('.button').setAttribute("disabled", "disabled");
    document.querySelector('.button').style.opacity = '0.7';

    document.querySelector('.agree_checkbox').onclick = function(){
        if (document.querySelector('.agree_checkbox').checked) {
            document.querySelector('.button').removeAttribute("disabled", "disabled");
            document.querySelector('.button').style.opacity = '1';
        }
        else {
            document.querySelector('.button').setAttribute("disabled", "disabled");
            document.querySelector('.button').style.opacity = '0.7';
        }
    }
}




// --------------------------- CONTACTS -------------------------------------
if($('#contactForm')){
    $('#contactForm').submit(function(e){
        e.preventDefault();
        var name = $('.contact_us_name').val();
        var email = $('.contact_us_email').val();
        var text = $('.contact_us_text').val();
        $('.contact_us_submit').addClass('button_loading');
        data = {
            'name': name,
            'email': email,
            'text': text,
        }

        $.ajax({
            url: "/contacts/",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            method : "post",
            dataType : "json",
            data : data,
            success: function (response) {
                $('.contact_us_submit').removeClass('button_loading');
                console.log(response['response'])
                $('.contact_us_submit_input').val(response['response']);
            },
            error: function (response) {
                alert('Error... Try again later.');
                $('.contact_us_submit').removeClass('button_loading');
            }
        });
        return false;
    })
}