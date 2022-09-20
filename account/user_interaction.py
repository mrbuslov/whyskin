from django.db.models.signals import post_save
from store import settings
import requests
from cosmetics.models import *
from aiogram import types
from .views import EmailThreading
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template


BOT_TOKEN = settings.TOKEN
buslov_id = settings.BUSLOV_TELEGRAM
admin_group_id = settings.ADMIN_GROUP_TELEGRAM
website_domain = 'https://whyskin.com.ua'


def created_order_func(instance):
    parse_message = f"🔥НОВЫЙ ЗАКАЗ!🔥\n"

    keyboard_markup = types.InlineKeyboardMarkup()
    press_btn = types.InlineKeyboardButton('Перейти', url=f"{website_domain}/only_for_admin/cosmetics/order/{instance.pk}/change/")
    keyboard_markup.row(press_btn)

    # https://www.youtube.com/watch?v=xFoUNDRVBYM&ab_channel=%D0%9C%D1%8D%D0%BB%D1%81%D0%B8%D0%BA-%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5
    # 7:37
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={admin_group_id}&text={parse_message}&parse_mode=HTML&reply_markup={keyboard_markup}")


def send_order_email_func(order):
    ordered_products = OrderItem.objects.filter(order=order)
    images = []
    for prod in ordered_products: images.append(Image.objects.filter(product=prod.product).first())
    ordered_products = list(zip(ordered_products, images))
    context = {
        'order': order,
        'ordered_products': ordered_products
    }


    email = order.author_email

    mail_title = f"Замовлення {order.order_num} на WhySkin"
    html = get_template('email/order.html').render(context)
    text = f'''
    WhySkin (https://whyskin.com.ua/) № замовлення: {order.order_num} щодня з 8:55 до 20:00
    ** Вітаємо, {order.author_name}!
    ------------------------------------------------------------
    Ми дуже цінуємо ❤️ Вас за те, що обрали нас!
    Найближчим часом ми зв'яжемося з Вами через дзвінок або месенджер
    Замовлення № {order.order_num} {order.published} '''
    for product, image in ordered_products:
        text += f'''
        (Фото товару - {image.image.url}) {product.product.name}
        {product.product.name} (https://whyskin.com.ua/{product.product.slug}/) Кількість: {product.quantity}
        {product.total_price} ₴
        '''
    if order.delivery_company == 'np':
        text += ' Стандартне пакування 7 ₴'
    elif order.delivery_company == 'pickup':
        text += ' Пакет-банан безкоштовно'
    
    text += f'''
    {int(order.total_price)} ₴
    Виникли додаткові запитання?
    Наші контакти: Номер телефону: +380(98) 622-50-33 (tel:+380986225033) Телеграм: @whyskin (https://t.me/whyskin)
    WhySkin - магазин корейської косметики з індивідуальним підходом❤️
    Завжди свіжі новинки для всіх типів шкіри!
    '''


    msg = EmailMultiAlternatives(
        mail_title,
        text,
        settings.EMAIL_HOST_USER,
        [email])
    msg.attach_alternative(html, "text/html")
    EmailThreading(msg).start()

    


# https://docs.djangoproject.com/en/4.1/ref/signals/#post-save
def created_order(sender, instance, created, **kwargs):
    if created == True: 
        created_order_func(instance)
        send_order_email_func(instance)

# post_save.connect(created_order, sender=Order) # этой строкой мы получаем сигнал о том, что пост был создан