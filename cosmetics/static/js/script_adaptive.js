/*---------------------------------- ДВИГАЕМ adaptive_header-------------------------------------------------------*/
var adaptive_header = document.querySelector(".adaptive_header");
var arr = [0];
window.addEventListener('scroll', ()=>{
    let scrolled = window.scrollY;
    arr.push(scrolled);
    for(let i=arr.length-1; i<=arr.length; i++){
        if(arr[i-1] > arr[i]){
            adaptive_header.classList.remove("adaptive_header_hide");
        }
        if(arr[i-1] < arr[i]){
            adaptive_header.classList.add("adaptive_header_hide");
        }        
    }
})

/*---------------------------------- HAMBURGER NAVIGATION -------------------------------------------------------*/

function open_close_menu(){
    var menu_overlay = document.querySelector('.menu_overlay');
    var menu = document.querySelector('.menu');
    var adaptive_header_menu = document.querySelector('.adaptive_header_menu');
    
    menu_overlay.classList.toggle('menu_overlay_show');
    menu.classList.toggle('menu_show');
    if($(adaptive_header_menu).css('zIndex') == -1){$(adaptive_header_menu).css('zIndex', '1000')}
    else{setTimeout(function(){$(adaptive_header_menu).css('zIndex', '-1')}, 350) }
}
function open_close_secondary_menu(this_menu){
    this_menu.toggleClass('menu_secondary_show'); // toggleClass вместо toggle, потому что работаем с jquery, а не с js
}
window.onload = function () {
    var adaptive_header_hamb = document.querySelector('.adaptive_header_hamb');
    var menu_overlay = document.querySelector('.menu_overlay');
    var menu = document.querySelector('.menu');
    var menu_toggle_close = document.querySelector('.menu_toggle_close');
    

    adaptive_header_hamb.addEventListener('click', function () {
    open_close_menu();
    });
    menu_overlay.addEventListener('click', function () {
    open_close_menu();
    });
    menu_toggle_close.addEventListener('click', function () {
    open_close_menu();
    });
    $('.menu_item_next').on('click', function () {
    open_close_secondary_menu($(this).next('.menu_secondary'));
    });
    $('.menu_toggle_secondary_menu').on('click', function () {
    open_close_secondary_menu($(this).closest('.menu_secondary'));
    });
}


/*---------------------------------- HAMBURGER NAVIGATION CATEGORIES -------------------------------------------------------*/
if($('.adaptive_menu_categ_dropdown')) {
    $('.adaptive_menu_categ_dropdown_ul').slideUp(); // прячем меню при начальной загрузке страницы
    $('.adaptive_menu_categ_dropdown').click(function() {  // при клике открываем
        $(this).next('.adaptive_menu_categ_dropdown_ul').slideToggle();
        $(this).find('img').toggleClass('arrow_up');
    });
  };



/*---------------------------------- РАБОТА СО СТРОКОЙ ПОИСКА -------------------------------------------------------*/
if(document.querySelector('.search_nav')){
    var search = document.querySelector('.search_nav');
    search.onclick = function(){
        document.querySelector('.main_dark_search').classList.toggle('mds_show');
        document.querySelector('.adaptive_header_search_cover').classList.toggle('sf_show');
    }
}

/*------------------------------------------------------- Убираем поле поиска, если щёлкаем вне него -------------------------------------------------------*/
if(document.querySelector('.main_dark_search')){
    document.querySelector('.main_dark_search').onclick = function(){
        search.onclick();
        if(document.querySelector('.more_filters_field').style.display != 'none'){
        document.querySelector('.more_filters').onclick();
        }
    }
}


if (window.innerWidth < 1367) {
    // Если мы на планшете, нам нужно открыть подкатегории, а не перейти по категории
    $('.header_category_main_a').on('click', function(e){
        e.preventDefault();
    })
}