/*

<!-- 

    ------------------------------------- TypeOfWarehouseRef ----------------------------------------------------------

        {
            "Ref": "6f8c7162-4b72-4b0a-88e5-906948c6a92f",
			"Description": "Parcel Shop",
			"DescriptionRu": "Parcel Shop"
		},
		{
			"Ref": "841339c7-591a-42e2-8233-7a0a00f0ed6f",
			"Description": "Поштове відділення",
			"DescriptionRu": "Почтовое отделение"
		},
		{
			"Ref": "95dc212d-479c-4ffb-a8ab-8c1b9073d0bc",
			"Description": "Поштомат ПриватБанку",
			"DescriptionRu": "Почтомат приват банка"
		},
		{
			"Ref": "9a68df70-0267-42a8-bb5c-37f427e36ee4",
			"Description": "Вантажне відділення",
			"DescriptionRu": "Грузовое отделение"
		},
		{
			"Ref": "f9316480-5f2d-425d-bc2c-ac7cd29decf0",
			"Description": "Поштомат",
			"DescriptionRu": "Почтомат"
		}
 -->
*/


$( document ).ready(function() {
    // так как у нас по дефолту Новая Почта
    $('#id_way_of_payment_0').closest('.way_of_payment_radio').show(); // показываем перевод на карту
    $('#id_way_of_payment_1').closest('.way_of_payment_radio').hide(); // скрываем наличные средства
    $('#id_way_of_payment_2').closest('.way_of_payment_radio').show(); // показываем налож. плат
    // // $('#id_author_patronymic').prop('required',true);
});



function request_to_nova_p(data, search_type, fill_field){
    data = JSON.stringify(data);
    response = null;

    $.ajax({
        type: 'POST',
        dataType: 'json',
        url: 'https://api.novaposhta.ua/v2.0/json/',
        data: data,
        // async:false,
        headers: {'Content-Type': 'application/json'},
        xhrFields: {withCredentials: false},
        success: function(res) {
            response = res;
            fill_in_searching_results(response, search_type, fill_field);
            $('.city_field').find('.subtitle_text_span span').removeClass('button_loading');
        },
    });
    return response;
}

function fill_in_searching_results(response, search_type='city', fill_field){
    if(response.success !== false && response.data[0] !== undefined && response.data[0].TotalCount !== 0){
        fill_field.show();
        var searching = null;
        var searching_selections = null;

        
        if(search_type === 'city'){
            searching = response.data[0].Addresses;
            var searching_selections = `<ul class="${search_type}_all_results">`;
            for(i in searching){
                searching_selections += `<li><p class="${search_type}_result_p">${searching[i].Present}</p><input type="hidden" value="${searching[i].MainDescription}" class="short_city_hidden"></li>`
            }
            searching_selections += '</ul>';
        }

        else if(search_type === 'warehouse'){
            searching = response.data;
            var searching_selections = '';
            for(i in searching){
                searching_selections += `<option value="${searching[i].Description}">№ ${searching[i].Number} - ${searching[i].ShortAddress}</option>`
            }
        }

        
        fill_field.html(searching_selections);
    }
    else{
        fill_field.hide();
    }
}



// Если у нас что-то есть в input, тогда ищем по тому, что там есть
$('#city_input').on('click', function(){
    if($(this).val() !== ''){
        data = {
            modelName: 'Address',
            calledMethod: 'searchSettlements',
            methodProperties: {
                CityName: $(this).val(),
                Limit: 50
            },
            apiKey: 'YOUR_API_KEY'
        }

        request_to_nova_p(data, 'city', $('#city_results'));
    }
});
// просто ищем город
$('#city_input').on('keyup', function(){
    data = {
        modelName: 'Address',
        calledMethod: 'searchSettlements',
        methodProperties: {
            CityName: $(this).val(),
            Limit: 50
        },
        apiKey: 'YOUR_API_KEY'
    }

    request_to_nova_p(data, 'city', $('#city_results')); 
});
// выбираем город и подгружаем отделения 
$(document).on("click", ".city_result_p", function () {
    $('#city_input').val($(this).text());
    $('#city_input_short').val($(this).parent().find('.short_city_hidden').val());
    $('#city_results').hide();
    $('.city_field').find('.subtitle_text_span span').addClass('button_loading');

    warehouse_categ = '';
    if(document.getElementById('in_warehouse').checked){warehouse_categ = "";} // Branch не работает(
    else{warehouse_categ = 'Postomat';}
    data = {
        modelName: 'Address',
        calledMethod: 'getWarehouses',
        methodProperties: {
            CityName: $('#city_input_short').val(),
            CategoryOfWarehouse: warehouse_categ,
            // TypeOfWarehouseRef:"9a68df70-0267-42a8-bb5c-37f427e36ee4",
            // TypeOfWarehouseRef:"841339c7-591a-42e2-8233-7a0a00f0ed6f",
        },
        apiKey: 'YOUR_API_KEY'
    }
    request_to_nova_p(data, 'warehouse', $('#warehouse_input'));
});


$('.delivery_checkbox').on('change', function(){
    if($(this).val() === 'np'){
        $('.delivery_info_np').show();
        $('.delivery_info_pickup').hide();
        $("#city_input").prop('required',true);
        $(".order_total_price").html($('.order_total_price_hidden').val() + ' <span>₴</span>');
        $(".order_goods_if_pickup").hide();
        $(".order_goods_if_np").show();
        
        $('#id_way_of_payment_0').closest('.way_of_payment_radio').show(); // показываем перевод на карту
        $('#id_way_of_payment_1').closest('.way_of_payment_radio').hide(); // скрываем наличные средства
        $('#id_way_of_payment_2').closest('.way_of_payment_radio').show(); // показываем налож. плат
        
        // $('#id_author_patronymic').prev('.subtitle_text_span').show();
        // $('#id_author_patronymic').show();
        // $('#id_author_patronymic').prop('required',true);
    }
    else if($(this).val() === 'pickup'){
        $('.delivery_info_np').hide();
        $('.delivery_info_pickup').show();
        $("#city_input").prop('required',false);
        $(".order_total_price").html(parseInt($('.order_total_price_hidden').val())-7 + ' <span>₴</span>');
        $(".order_goods_if_pickup").show();
        $(".order_goods_if_np").hide();

        $('#id_way_of_payment_0').closest('.way_of_payment_radio').show(); // показываем перевод на карту
        $('#id_way_of_payment_1').closest('.way_of_payment_radio').show(); // показываем наличные средства
        $('#id_way_of_payment_2').closest('.way_of_payment_radio').hide(); // скрываем налож. плат
        
        // $('#id_author_patronymic').prev('.subtitle_text_span').hide();
        // $('#id_author_patronymic').hide();
        // $('#id_author_patronymic').prop('required',false);
    }
});

$('.delivery_way_checkbox').on('change', function(){
    if($(this).val() === 'В отделение'){
        // $('#id_author_patronymic').prev('.subtitle_text_span').show();
        // $('#id_author_patronymic').show();
        // $('#id_author_patronymic').prop('required',true);
    }
    else if($(this).val() === 'В почтомат'){
        // $('#id_author_patronymic').prev('.subtitle_text_span').hide();
        // $('#id_author_patronymic').hide();
        // $('#id_author_patronymic').prop('required',false);
    }
});


$('#id_author_phone').on('click', function(){ // если мы только кликнули по полю, переместим курсор на начало
    if( $(this).val() === '+380(__) ___-__-__'){this.selectionStart = this.selectionEnd = 5;}
})
$(function(){
    $("#id_author_phone").mask("+380(99) 999-99-99", {
        // completed: function(){ console.log("Вы ввели номер: " + this.val()); }
    });
});




if($('.way_of_payment_radio')){
    $('.radio_pay_changed').first().css('background', '#6F9D70');
    $('.way_of_payment_radio').on( "click", function(){
        $('.radio_pay_changed').css('background', '#fff');
        $(this).find('.radio_pay_changed').css('background', '#6F9D70');
    });
}
