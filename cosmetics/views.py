import functools
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .middleware import CartAndLiked
from .models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from googletrans import Translator
import html2text
from django.utils.translation import gettext_lazy as _
from django.template.defaulttags import register
from django.db.models import Q
from account.user_interaction import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import os
import random
from django.contrib.admin.views import decorators
from datetime import datetime

'''
https://developers.novaposhta.ua/
https://new.novaposhta.ua/dashboard/settings/developers
Точка входа -> https://api.novaposhta.ua/v2.0/json/
'''
'''
https://dev.ukrposhta.ua/documentation
https://ukrposhta.ua/ecom/0.0.1
'''

'''
--- Для клонирования объекта ---
obj = Product.objects.get(pk=8)
obj.pk=None
obj.vendor_code = 123456
obj.slug = "asdawdad"
obj.save()
'''
'''
pip install googletrans==3.1.0a0
'''

def translate_str(string):
    string_trans = ''
    if get_language() == 'uk':
        try:
            # You can get about 1000 requests / hour without hitting the req/IP block limit. Also, individual requests are limited to less than 5000 characters per request
            translator = Translator()
            string_trans = translator.translate(string, dest='ru').text
        except Exception as e: print(e)

        return {'uk':string, 'ru':string_trans}
    elif get_language() == 'ru':
        try:
            # You can get about 1000 requests / hour without hitting the req/IP block limit. Also, individual requests are limited to less than 5000 characters per request
            translator = Translator()
            string_trans = translator.translate(string, dest='uk').text
        except Exception as e: print(e)

        return {'ru':string, 'uk':string_trans}


def get_product_zip_with_images(queryset, item_add_to_cart=False, request=None):
    if len(queryset) == 0: return []
    images = []
    is_added_to_cart = []
    is_added_to_liked = []
    if item_add_to_cart:
        for prod in queryset: 
            images.append(Image.objects.filter(product=prod).first())
            is_added_to_cart.append(str(prod.vendor_code) in request.session.get('carted_prod_vend_codes', '').split(';'))
            is_added_to_liked.append(str(prod.vendor_code) in request.session.get('liked_prod_vend_codes', '').split(';'))
        return list(zip(queryset, images, is_added_to_cart, is_added_to_liked))
    else:
        for prod in queryset: images.append(Image.objects.filter(product=prod).first())
        return list(zip(queryset, images))

def return_404(request):
    response = render(request, 'others/404.html')
    response.status_code = 404
    return response


def staff_member_required(view_func): # переопределим декоратор
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('cosmetics:index')
    return functools.wraps(view_func)(_checklogin)

decorators.staff_member_required = staff_member_required 






def search(request):
    if 'search_product' in request.GET:
        search_product = request.GET['search_product'].strip().lower()
        products = Product.objects.filter(Q(name__icontains=search_product) | Q(description__icontains=search_product) | Q(category__name__icontains=search_product))

        paginator = Paginator(products, 16)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        response = paginator.page(page_num)
        
        products = get_product_zip_with_images(response, True, request)

        context = {
            'search_product':search_product, 
            'products':products,
            'page':page,
        }
        return render(request, 'cosmetics/search.html', context)
    else:
        return redirect('cosmetics:index')


def index(request):
    index_products = Product.objects.order_by('?')[:10]
    context = {
        'products':get_product_zip_with_images(index_products, True, request),
    }
    return render(request, 'cosmetics/index.html', context)

def test(request):
    # print(request.session.get('carted_prod_vend_codes', None))
    # del request.session['carted_prod_vend_codes']
    # print(request.session.get('author_name', None))
    # print(request.session.get('carted_prod_vend_codes', '').split(';'))
    
    # # https://developers.novaposhta.ua/view/model/a90d323c-8512-11ec-8ced-005056b2dbe1/method/a965630e-8512-11ec-8ced-005056b2dbe1
    # {
    #     "apiKey": "YOUR_API_KEY",
    #     "modelName": "InternetDocument",
    #     "calledMethod": "save",
    #     "methodProperties": {
    #         "PayerType" : "Recipient", # Sender, Recipient, ThirdPerson
    #         "PaymentMethod" : "NonCash", # Cash/NonCash
    #         "DateTime" : "30.08.2022",
    #         "CargoType" : "Cargo",
    #         "VolumeGeneral" : "0.003672", # 24x17x9
    #         "Weight" : "1",
    #         "ServiceType" : "WarehouseWarehouse",  # DoorsDoors, DoorsWarehouse, WarehouseWarehouse, WarehouseDoors 
    #         "SeatsAmount" : "1",
    #         "Description" : "Косметика",
    #         "Cost" : "200",
    #         "SendersPhone" : "380983435878",
    #         "RecipientsPhone" : "+380(98) 343-58-78".replace('+','').replace(' ','').replace('-','').replace(')','').replace('(',''),

    #         # київ
    #         "CitySender" : "e718a680-4b33-11e4-ab6d-005056801329",
    #         "Sender" : "00000000-0000-0000-0000-000000000000",
    #         "SenderAddress" : "00000000-0000-0000-0000-000000000000",
    #         "ContactSender" : "00000000-0000-0000-0000-000000000000",

    #         "CityRecipient" : "00000000-0000-0000-0000-000000000000",
    #         "Recipient" : "00000000-0000-0000-0000-000000000000",
    #         "RecipientAddress" : "00000000-0000-0000-0000-000000000000",
    #         "ContactRecipient" : "00000000-0000-0000-0000-000000000000",
    #     }
    # }

    # index_products = Product.objects.order_by('?')[:10]
    # context = {
    #     'products':get_product_zip_with_images(index_products, True, request),
    # }
    return render(request, 'others/test.html')
    # context = {
    #     'ordered_products':get_product_zip_with_images(index_products),
    # }
    # return render(request, 'email/order.html', context)


def category(request, category):
    try:
        category_obj = Category.objects.get(slug=category)
    except:
        return return_404(request)    
        
    product_obj = Product.objects.filter(Q(category__name__in=list(category_obj.children.all())) | Q(category__name=category_obj.name))
    
    paginator = Paginator(product_obj, 16)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    response = paginator.page(page_num)

    products = get_product_zip_with_images(response, True, request)

    product_category_parents = []
    categ = category_obj
    while categ.parent != None:
        product_category_parents.append(categ.parent)
        categ = categ.parent
    product_category_parents.reverse()

    context = {
        'products':products,
        'page':page,
        'category':category_obj,
        'product_category_parents': product_category_parents
    }
    return render(request, 'cosmetics/cosmetics_list.html', context)


def product(request, product):
    try:
        product_obj = Product.objects.get(slug=product)
    except:
        return return_404(request)
    images = Image.objects.filter(product=product_obj)
    related_products = []

    # ищем подобные этому продукты
    related_by_name = Product.objects.filter(name__icontains = str(product_obj.name)[:int(len(product_obj.name))//2]).exclude(id=product_obj.id) # берём, скажем, первую половину названия
    if related_by_name.count() != 0: 
        for obj in related_by_name: related_products.append(obj)

    related_by_category = Product.objects.filter(category = product_obj.category).exclude(id=product_obj.id).exclude(id__in=[_id.id for _id in related_products])
    if related_by_category.count != 0 and len(related_products) <= 10:
        for obj in related_by_category: 
            if len(related_products) <= 10:
                related_products.append(obj)
            else:
                break

    related_by_manufacturer = Product.objects.filter(manufacturer = product_obj.manufacturer).exclude(id=product_obj.id).exclude(id__in=[_id.id for _id in related_products])
    if related_by_manufacturer.count != 0 and len(related_products) <= 10:
        for obj in related_by_manufacturer: 
            if len(related_products) <= 10:
                related_products.append(obj)
            else:
                break


    if str(product_obj.vendor_code) not in request.session.get('carted_prod_vend_codes', '').split(';'):
        product_in_cart = False
    else:
        product_in_cart = True
    if str(product_obj.vendor_code) not in request.session.get('liked_prod_vend_codes', '').split(';'):
        product_in_liked = False
    else:
        product_in_liked = True
            
    context = {
        'product':product_obj,
        'images':images,
        'related_products':related_products,
        'product_in_cart':product_in_cart,
        'product_in_liked':product_in_liked,
    }
    return render(request, 'cosmetics/product.html', context)

@staff_member_required
def my_admin(request):
    orders = Order.objects.all()
    return render(request, 'admin_fld/admin_index.html', {'orders':orders})

@staff_member_required
def add_new_product(request):

    if request.is_ajax():
        category_id = request.GET.get('category_id', None)
        images = request.FILES.getlist('img')

        if category_id:
            if category_id == '':
                return JsonResponse(data={
                    'subcategories': 'empty',
                })

            category = Category.objects.get(id=int(category_id))

            subcategories = {}
            for subcat in category.children.all():
                subcategories[subcat.id] = subcat.name

            return JsonResponse(data={
                'subcategories':subcategories,
            })
        elif images:
            uploaded_images = {}
            for val in images:
                uploaded_image = Image.objects.create(image=val)
                uploaded_images[uploaded_image.id] = str(uploaded_image.image.url)

            return JsonResponse(data={
                'uploaded_images':uploaded_images,
            })


    if request.method =='POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            try:
                product.category = Category.objects.get(id=int(request.POST['subcategory']))
            except:
                product.category = Category.objects.get(id=int(request.POST['category']))

            trans_name = translate_str(product.name)
            trans_description = translate_str(html2text.html2text(product.description).replace('[','').replace(']','').replace('*','').strip())
            trans_country = translate_str(product.country)
            trans_active_components = translate_str(product.active_components)
            trans_purpose = translate_str(product.purpose)
            trans_skin_type = translate_str(product.skin_type)
            trans_how_to_use = translate_str(product.how_to_use)

            product.name_uk = trans_name['uk']
            product.name_ru = trans_name['ru']
            if get_language() == 'uk':
                product.description_uk = product.description
                product.description_ru = trans_description['ru']
            elif get_language() == 'ru':
                product.description_ru = product.description
                product.description_uk = trans_description['uk']
            product.country_uk = trans_country['uk']
            product.country_ru = trans_country['ru']
            product.active_components_uk = trans_active_components['uk']
            product.active_components_ru = trans_active_components['ru']
            product.purpose_uk = trans_purpose['uk']
            product.purpose_ru = trans_purpose['ru']
            product.skin_type_uk = trans_skin_type['uk']
            product.skin_type_ru = trans_skin_type['ru']
            product.how_to_use_uk = trans_how_to_use['uk']
            product.how_to_use_ru = trans_how_to_use['ru']
            
            product.save()
            
            uploaded_images_ids = request.POST['uploaded_images_ids'].split(';')
            uploaded_images_ids = [int(i) for i in uploaded_images_ids if i!='']
            counter = 1
            for image in Image.objects.filter(id__in = uploaded_images_ids):
                image.product = product
                # меняем название фото на название продукта для seo
                old_name = str(image.image)
                new_name = '/'.join(old_name.split('/')[:-1]) + '/' +  slugify(product.name) + '-' + str(counter) + '.' + 'jpg' #+ str(image.image).split('/')[-1].split('.')[-1]
                
                if os.path.exists(new_name): new_name = '/'.join(old_name.split('/')[:-1]) + '/' +  slugify(product.name) + '-' + str(random.randint(5, 20)) + '.' + 'jpg'
                
                os.rename(old_name, new_name) # ставим тут, потому что, когда мы меняем название image.image = new_name, django-cleanup библиотека удаляет изображение
                image.image = new_name
                image.save()
                counter += 1

            # return redirect('cosmetics:all_products_admin')
            return redirect('admin:cosmetics_product_change', product.id)
    else:
        form = ProductForm()
        categories = Category.objects.filter(parent=None)
        return render(request, 'admin_fld/add_product.html', {'form':form, 'categories':categories})

@staff_member_required
def all_products_admin(request):
    return render(request, 'admin_fld/all_products_admin.html')


@csrf_exempt
def cart(request):
    if request.is_ajax():
        prod_slug = request.POST.get('prod_slug', None)
        product = Product.objects.get(slug=prod_slug)
        status = ''
        action = ''
        button_htmlContent = ''
        if get_language() == 'uk': goto_url = '/cart/'
        elif get_language() == 'ru': goto_url = '/ru/cart/'

        # если в сессии у нас ничего нет, заполним данными с аккаунта пользователя
        if request.user.is_authenticated and request.session.get('carted_prod_vend_codes', '') == '':
            request.session['carted_prod_vend_codes'] = ';'.join([str(cart_obj.vendor_code) for cart_obj in request.user.carted.all()])
   
        carted_prod_vend_codes = request.session.get('carted_prod_vend_codes', '')
        if carted_prod_vend_codes != '':
            carted_prod_vend_codes = carted_prod_vend_codes.split(';')
            if str(product.vendor_code) in carted_prod_vend_codes:
                carted_prod_vend_codes.remove(str(product.vendor_code))
                carted_prod_vend_codes = ';'.join(carted_prod_vend_codes)
                request.session['carted_prod_vend_codes'] = str(carted_prod_vend_codes)

                status = 'remove'
                action = _('Удалено с корзины')
                button_htmlContent = '<div>'+_('Добавить в корзину') + '</div> <span>(' + _('и смотреть дальше')+')</span></a>'
            else:
                carted_prod_vend_codes.append(str(product.vendor_code))
                carted_prod_vend_codes = ';'.join(carted_prod_vend_codes)
                request.session['carted_prod_vend_codes'] = str(carted_prod_vend_codes)

                status = 'add'
                action = _('Добавлено в корзину')
                button_htmlContent = _('Добавлено в корзину') + '!✅'
        else:
            request.session['carted_prod_vend_codes'] = str(product.vendor_code)

            status = 'add'
            action = _('Добавлено в корзину')
            button_htmlContent = _('Добавлено в корзину') + '!✅'


        if request.user.is_authenticated:
            if request.user.carted.filter(id=product.id).exists():
                request.user.carted.remove(product)
            else:
                request.user.carted.add(product)


        return JsonResponse(data={
            'status': status,
            'action': action,
            'button_htmlContent':button_htmlContent,
            'goto_url':goto_url,
        })
    else:
        vendor_codes = []
        for v_c in request.session.get('carted_prod_vend_codes', '').split(';'):
            try:
                v_c = int(v_c)
                vendor_codes.append(v_c)
            except: pass

        products = Product.objects.filter(vendor_code__in = vendor_codes )
        all_products = get_product_zip_with_images(products)

        total_price = 0
        for prod in products: total_price+=prod.price
        
        return render(request, 'cosmetics/cart.html',{'all_products':all_products, 'total_price':total_price})

@csrf_exempt
def liked(request):
    if request.is_ajax():
        prod_slug = request.POST.get('prod_slug', None)
        product = Product.objects.get(slug=prod_slug)
        status = ''
        action = ''
        button_htmlContent = ''
        if get_language() == 'uk': goto_url = '/liked/'
        elif get_language() == 'ru': goto_url = '/ru/liked/'

        # если в сессии у нас ничего нет, заполним данными с аккаунта пользователя
        if request.user.is_authenticated and request.session.get('liked_prod_vend_codes', '') == '':
            request.session['liked_prod_vend_codes'] = ';'.join([str(cart_obj.vendor_code) for cart_obj in request.user.liked.all()])
   
        liked_prod_vend_codes = request.session.get('liked_prod_vend_codes', '')
        if liked_prod_vend_codes != '':
            liked_prod_vend_codes = liked_prod_vend_codes.split(';')
            if str(product.vendor_code) in liked_prod_vend_codes:
                liked_prod_vend_codes.remove(str(product.vendor_code))
                liked_prod_vend_codes = ';'.join(liked_prod_vend_codes)
                request.session['liked_prod_vend_codes'] = str(liked_prod_vend_codes)

                status = 'remove'
                action = _('Удалено с') + ' ❤️'
                button_htmlContent = '<div>'+_('Добавить в') + ' ❤️' + '</div> <span>(' + _('и смотреть дальше')+')</span></a>'
            else:
                liked_prod_vend_codes.append(str(product.vendor_code))
                liked_prod_vend_codes = ';'.join(liked_prod_vend_codes)
                request.session['liked_prod_vend_codes'] = str(liked_prod_vend_codes)

                status = 'add'
                action = _('Добавлено в') + ' ❤️'
                button_htmlContent = _('Добавлено в') + ' ❤️' + '!✅'
        else:
            request.session['liked_prod_vend_codes'] = str(product.vendor_code)

            status = 'add'
            action = _('Добавлено в') + ' ❤️'
            button_htmlContent = _('Добавлено в') + ' ❤️' + '!✅'


        if request.user.is_authenticated:
            if request.user.liked.filter(id=product.id).exists():
                request.user.liked.remove(product)
            else:
                request.user.liked.add(product)


        return JsonResponse(data={
            'status': status,
            'action': action,
            'button_htmlContent':button_htmlContent,
            'goto_url':goto_url,
        })
    else:
        vendor_codes = []
        for v_c in request.session.get('liked_prod_vend_codes', '').split(';'):
            try:
                v_c = int(v_c)
                vendor_codes.append(v_c)
            except Exception as e: print(e)

        products = Product.objects.filter(vendor_code__in = vendor_codes )
        all_products = get_product_zip_with_images(products, True, request)
        
        return render(request, 'cosmetics/liked.html',{'all_products':all_products})


def order(request):
    if request.user.is_authenticated:
        if request.user.first_name == '' or request.user.first_name == None:
            form = OrderForm(initial={
                'author_name': request.session.get('author_name', ''), 
                'author_surname': request.session.get('author_surname', ''), 
                'author_phone': request.session.get('author_phone', ''), 
                'author_email': request.session.get('author_email', ''), 
            })
        else:
            form = OrderForm(initial={
                'author_name': request.user.first_name, 
                'author_surname': request.user.last_name, 
                'author_phone': request.user.phone_number, 
                'author_email': request.user.email, 
            })
    else:
        form = OrderForm(initial={
            'author_name': request.session.get('author_name', ''), 
            'author_surname': request.session.get('author_surname', ''), 
            'author_phone': request.session.get('author_phone', ''), 
            'author_email': request.session.get('author_email', ''), 
        })

    packaging_materials_for_np = {
        _('Стандартная упаковка'): 7,
    }
    packaging_materials_for_pickup = {
        _('Пакет-банан'): 0,
    }

    # если есть в запросе id товара, то оформим только его 
    if request.GET != {}:
        vendor_code = request.GET['vendor_code']
        if not Product.objects.filter(vendor_code=vendor_code).exists():
            return render(request, 'cosmetics/order.html', {'error':_('К сожалению, такого товара мы не нашли') + ' 😞'})
        
        product = Product.objects.get(vendor_code=vendor_code)
        image = Image.objects.filter(product=product).first()
        product_quantity = ['1']
        my_product = list(zip([product],[image],product_quantity))
        
        request.session['order_vendor_codes'] = vendor_code
        request.session['order_product_quantity'] = ';'.join(product_quantity)

        total_price = int(product.price)
        total_price += 7 # потому что у нас по дефолту стоит Новая почта

        context = {
            'packaging_materials_for_np': packaging_materials_for_np,
            'packaging_materials_for_pickup': packaging_materials_for_pickup,
            'products': my_product, 
            'total_price': total_price,
            'form':form
        }
        return render(request, 'cosmetics/order.html', context)
    # если post - перешли с корзины
    elif request.method == 'POST':
        carted_prod_vend_codes = request.session.get('carted_prod_vend_codes', '')
        products = Product.objects.filter(vendor_code__in = [int(prod_vc) for prod_vc in carted_prod_vend_codes.split(';')])
        total_price = 0

        product_quantity = request.POST.getlist('product_quantity')
        vendor_codes = []
        images = []
        for i, prod in enumerate(products):
            vendor_codes.append(str(prod.vendor_code))
            total_price += int(prod.price) * int(product_quantity[i]) 
            images.append(Image.objects.filter(product= prod).first())
        my_product = list(zip(products, images, product_quantity))
        total_price += 7 # потому что у нас по дефолту стоит Новая почта

        request.session['order_vendor_codes'] = ';'.join(vendor_codes)
        request.session['order_product_quantity'] = ';'.join(product_quantity)


        context = {
            'packaging_materials_for_np': packaging_materials_for_np,
            'packaging_materials_for_pickup': packaging_materials_for_pickup,
            'products': my_product, 
            'total_price': total_price,
            'form':form
        }
        return render(request, 'cosmetics/order.html', context)
    # если ничего нет, то перейдём в корзину
    else:
        return redirect('cosmetics:cart')


def order_success(request):
    if request.method == 'POST':
        form = OrderForm(data=request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # request.session['author_name']
            
            order.delivery_company = request.POST.get('delivery_checkbox', 'np')
            order.delivery_way = request.POST.get('delivery_way_checkbox', '')
            order.delivery_city = request.POST.get('city_input', '')
            order.delivery_point = request.POST.get('delivery_point_input', '')
            request.session['author_name'] = order.author_name
            request.session['author_surname'] = order.author_surname
            request.session['author_phone'] = order.author_phone
            request.session['author_email'] = order.author_email
            order.save()            
            
            total_price = 0
            products_codes = request.session.get('order_vendor_codes', '')
            order_product_quantity = request.session.get('order_product_quantity', '').split(';')
            products = Product.objects.filter(vendor_code__in=products_codes.split(';'))
            for i, prod in enumerate(products): 
                OrderItem.objects.create(product=prod, order=order, quantity=int(order_product_quantity[i]))
                total_price += int(prod.price) * int(order_product_quantity[i])
            if order.delivery_company == 'np': total_price += 7
            order.total_price = total_price
            if order.delivery_company == 'pickup': order.delivery_way = ''

            order.save()  

            # отправляем сообщения о товаре
            created_order_func(order)
            send_order_email_func(order)

            # очищаем товары в корзине: в сессии и в аккаунте
            if request.session.get('carted_prod_vend_codes', None): del request.session['carted_prod_vend_codes']
            if request.user.is_authenticated: request.user.carted.clear()

            return render(request, 'cosmetics/order_success.html', {'order_num':order.order_num})
        else:
            return render(request, 'cosmetics/order_success.html', {'error':True})
    else:
        return redirect('cosmetics:cart')



import html2text
from .models import WhySkinBlog
def blog(request):
    blog_obj = WhySkinBlog.objects.filter(status = 'published')
    paginator = Paginator(blog_obj, 20)

    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    
    yesterday_date = str(datetime.today().date().day-1).zfill(2) + '.' + str(datetime.today().date().month).zfill(2) + '.' + str(datetime.today().date().year).zfill(2) # для того, чтобы вместо дня 1 марта превратить в 01 марта

    context={
        'blog_obj':response, 
        'yesterday_date': yesterday_date,
    }

    return render(request, 'others/blog.html', context)

from django.db.models import F
def blog_post(request, slug):
    if WhySkinBlog.objects.filter(slug=slug).exists:
        blog_obj = WhySkinBlog.objects.get(slug=slug)
        WhySkinBlog.objects.filter(slug=slug).update(views=F('views')+1)
        return render(request, 'others/blog_post.html', {'blog_obj':blog_obj, 'current_lang':get_language()})
    else:
        return redirect('account:blog')


@staff_member_required
def add_blog_post(request):
    if request.method =='POST':
        form = WhySkinBlogForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.status = 'published'
            trans_title = translate_str(post.title)
            trans_content = translate_str(post.content)
            post.title_uk = trans_title['uk']
            post.title_ru = trans_title['ru']
            post.content_uk = trans_content['uk']
            post.content_ru = trans_content['ru']

            post.save()

            return redirect('cosmetics:blog')
        else:
            return redirect('cosmetics:add_blog_post')
    else:
        form = WhySkinBlogForm()
        context={
            'form':form,
        }       
        return render(request, 'others/blog_post_add.html', context) 




def handler400_error(request, *args, **argv):
    return render(request, "others/400.html")
def handler403_error(request, *args, **argv):
    return render(request, "others/403.html")
def handler404_error(request, *args, **argv):
    return render(request, "others/404.html", status=404)
def handler500_error(request, *args, **argv):
    return render(request, "others/500.html")

def privacy_policy(request):
    return render(request, "others/privacy_policy.html")
def contract_offer(request):
    return render(request, "others/contract_offer.html")
def exchange_and_return(request):
    return render(request, "others/exchange_and_return.html")
@csrf_exempt
def contacts(request):
    if request.is_ajax():
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        text = request.POST.get('text', None)
        
        text = f'Вопрос от посетителя: \n\n<strong>Имя</strong> - {name}\n<strong>Email/Номер телефона</strong> - {email}\n<strong>Вопрос</strong> - {text}' 
        requests.get(f"https://api.telegram.org/bot{settings.TOKEN}/sendMessage?chat_id={settings.ADMIN_GROUP_TELEGRAM}&text={text}&parse_mode=HTML")

        return JsonResponse(data={
            'response': _('Отправлено!'),
        })
    else:
        return render(request, "others/contacts.html")
def delivery_and_payment(request):
    return render(request, "others/delivery_and_payment.html")


def error(request):
    1/0
    # return render(request, "others/exchange_and_return.html")