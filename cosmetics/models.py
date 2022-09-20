import os
from typing import OrderedDict
from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
import datetime
from django.urls import reverse
from django.contrib.sitemaps import ping_google
import uuid
# from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
# from multiselectfield import MultiSelectField
from django.utils.translation import get_language
from pytils.translit import slugify # djangoвская slugify не принимает кирилицу, поэтому пользоваться этой
from PIL import Image as PIL_Image, ExifTags
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField





class Category(models.Model):
    name = models.CharField(max_length=100,db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Ссылка')
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    # Изменение нашей модели для админ-панели
    class Meta:
        verbose_name_plural='5. Рубрики' # verbose - подробный
        verbose_name= 'Рубрика'
        ordering=['id']
        
    # мы можем сделать подобным образом, так как у нас поле одно, а не несколько, как в Board(title,content...)
    def __str__(self):
        return self.name

    def get_absolute_url(self): # sitemap
        if get_language() == 'uk':
            return f'/product/{self.slug}'
        else:
            return f'/ru/product/{self.slug}'

            
    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    def get_all_parents(self):
        parents = [self]
        if self.parent is not None:
            parent = self.parent
            parents.extend(parent.get_all_parents())
        return parents



class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique = True,verbose_name='Ссылка')
    description = RichTextField(max_length=7500, verbose_name='Описание') 
    category = models.ForeignKey('cosmetics.Category', on_delete=models.SET_NULL, verbose_name='Рубрика', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Старая Цена', blank=True, null=True)
    vendor_code = models.PositiveIntegerField(unique = True, db_index=True, verbose_name='Артикул (код товара)', default=1000)
    warehouse_amount = models.PositiveIntegerField(verbose_name='Кол-во товара на складе', default='1')
    
    country = models.CharField(max_length=200, verbose_name='Страна')
    manufacturer = models.CharField(max_length=200, verbose_name='Производитель')
    active_components = models.CharField(max_length=500, verbose_name='Активные компоненты', blank=True, null=True)
    purpose = models.CharField(max_length=200, verbose_name='Предназначение', blank=True, null=True)
    skin_type = models.CharField(max_length=200, verbose_name='Тип кожи', blank=True, null=True)
    how_to_use = models.TextField(max_length=7500, verbose_name='Способ применения', blank=True, null=True)


    MEASURE_CHOICES = (
        ('ml', 'мл'),
        ('mg', 'мг'),
        ('g', 'г'),
        ('l', 'л'),
        ('kg', 'кг'),
        ('thing', 'шт'),
    )
    volume = models.PositiveIntegerField(verbose_name='Объём', blank=True, null=True)
    measure = models.CharField(max_length=20, choices=MEASURE_CHOICES, default='ml', blank=True, null=True)

    STATUS_CHOICES = (
        ('present', 'Товар есть ✅'),
        ('not_present', 'Товара нет ❌'),
        ('waiting', 'Ожидается'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    

    # Изменение нашей модели для админ-панели
    class Meta:
        verbose_name_plural='3. Товары' # verbose - подробный
        verbose_name= 'Товар'
        # ordering=['-published']
        ordering = ['-id']
    

    def __str__(self):
        return self.name

    def get_absolute_url(self): # sitemap
        if get_language() == 'uk':
            return f'/product/{self.slug}'
        else:
            return f'/ru/product/{self.slug}'

    def save(self,  *args, **kwargs):
        if self._state.adding:
            last_vendor_code = Product.objects.all().aggregate(largest=models.Max('vendor_code'))['largest']
            if last_vendor_code is not None:
                self.vendor_code = last_vendor_code + 1

            
            if Product.objects.filter(name=self.name.strip()).exists():
                self.slug = slugify(self.name) + '_' + str(uuid.uuid4()).replace('-','')[:7]
            else:
                if Product.objects.filter(slug=slugify(self.name)).exists():
                    self.slug = slugify(self.name) + '_' + str(uuid.uuid4()).replace('-','')[:7]
                else:
                    self.slug = slugify(self.name)

        super(Product, self).save(*args, **kwargs)

        try: 
            ping_google(sitemap_url='/sitemap.xml', sitemap_uses_https=True) # Вы можете захотеть «пинговать» Google, когда ваша карта сайта изменится, чтобы он знал, что нужно переиндексировать ваш сайт
        except Exception: 
            print('cannot ping Google')
            raise Exception('cannot ping Google')

    # Чтобы в админ-панели отображалось фото
    def image_tag(self):
        photos = f''
        objects = Image.objects.filter(product=self.id)
        for obj in objects:
            photos += f'<a href="{obj.image.url}"><img src="{obj.image.url}" width="150px" style="margin: 0 10px" /></a>'
       
        return mark_safe(photos)
    image_tag.short_description = 'Изображения'
    image_tag.allow_tags = True



    def split_active_components(self): # использовано в product.html
        return self.active_components.split(',')
    def get_prod_img_url(self): # использовано в product.html
        img_obj = Image.objects.filter(product=self.id)[0]
        return img_obj.image.url

    def is_liked(self,**kwargs): # использовано в product.html
        print(kwargs.pop('request'))
        # return img_obj.image.url



class Order(models.Model):
    order_num = models.PositiveIntegerField(unique = True, db_index=True, verbose_name='Номер заявки', default=1000)
    comment = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Комментарий') 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая цена', default=0)
    # ordered_prices = models.TextField(max_length=2000, verbose_name='Цены товаров при заказе') 
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано') 

    author_phone = models.CharField(max_length=20, verbose_name='Номер телефона') 
    author_email = models.EmailField(verbose_name='Email', null=True) 
    author_name = models.CharField(max_length=100, verbose_name='Имя') 
    author_surname = models.CharField(max_length=100, verbose_name='Фамилия')
    # author_patronymic = models.CharField(max_length=100, verbose_name='Отчество', null=True, blank=True)

    DELIVERY_COMPANY_CHOICES = (
        ('np', _('Новая Почта')),
        ('ukrp', _('Укрпочта')),
        ('pickup', _('Самовывоз')),
    )
    delivery_company = models.CharField(max_length=20, choices=DELIVERY_COMPANY_CHOICES, verbose_name='Способ доставки', default='np')
    delivery_city = models.CharField(max_length=100, verbose_name='Город доставки', null=True, blank=True)
    delivery_way = models.CharField(max_length=100, verbose_name='Отделение/Почтомат', null=True, blank=True)
    delivery_point = models.CharField(max_length=300, verbose_name='Отделение доставки', null=True, blank=True)

    WAY_OF_PAYMENT_CHOICES = (
        ('card', _('Оплата на карту')),
        ('cash', _('Наличные средства')),
        ('cod', _('Наложенный платёж')), # cod - Cash on Delivery
    )
    way_of_payment = models.CharField(max_length=20, choices=WAY_OF_PAYMENT_CHOICES, verbose_name='Вид оплаты', default='card')

    STATUS_CHOICES = (
        ('confirmed', _('Подтверждён')),
        ('considering', _('На рассмотрении')),
        ('paid', _('Оплачен')),
        ('rejected', _('Отклонён')),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='considering')


    class Meta:
        verbose_name_plural='1. Заказы' # verbose - подробный
        verbose_name= 'Заказ'
        ordering=['-published']


    def __str__(self):
        return str(self.order_num)

    def save(self,  *args, **kwargs):
        if self._state.adding:
            last_order_num = Order.objects.all().aggregate(largest=models.Max('order_num'))['largest']
            if last_order_num is not None:
                self.order_num = last_order_num + 1

        super(Order, self).save(*args, **kwargs)

    # Чтобы в админ-панели отображались заказанные товары
    def order_item_tag(self):
        order_item = f''
        objects = OrderItem.objects.filter(order=self.id)
        order_item += '<table>'
        order_item += '''<tr>
                            <th>Продукт</th>
                            <th></th>
                            <th>Кол-во</th>
                            <th>Кол-во на складе</th>
                            <th>Цена</th>
                            <th>Сумма</th>
                        </tr>'''
        for obj in objects:
            order_item += f'''
            
            <tr>
                <td><a href="/admin/cosmetics/orderitem/{obj.id}/change/">{obj.product.name}</a></td>
                <td style="text-align:center;"><a href="/admin/cosmetics/product/{obj.product.id}/change/">➡️</a></td>
                <td style="text-align:center;">{obj.quantity}</td>
                <td style="text-align:center;">{obj.product.warehouse_amount}</td>
                <td style="text-align:center;">{int(obj.product.price)}</td>
                <td style="text-align:center;">{int(obj.product.price) * int(obj.quantity)}</td>
            </tr>

            '''
        if self.delivery_company == 'np':
            order_item += f'''
            <tr>
                <td>Упаковка от НП</td>
                <td style="text-align:center;"></td>
                <td style="text-align:center;">1</td>
                <td style="text-align:center;"></td>
                <td style="text-align:center;">7</td>
                <td style="text-align:center;">7</td>
            </tr>
            '''
        elif self.delivery_company == 'pickup':
            order_item += f'''
            <tr>
                <td>Пакет-банан</td>
                <td style="text-align:center;"></td>
                <td style="text-align:center;">1</td>
                <td style="text-align:center;"></td>
                <td style="text-align:center;">0</td>
                <td style="text-align:center;">0</td>
            </tr>
            '''
        order_item += f'<tr><th></th><th></th><th></th><th></th><th></th><th>{int(self.total_price)}</th></tr>'
        order_item += '</table>'

        return mark_safe(order_item)
    order_item_tag.short_description = 'Товары в заказе'
    order_item_tag.allow_tags = True

        

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        verbose_name_plural='2. Товары в заказе' 
        verbose_name= 'Товары'

    def __str__(self):
        return self.product.name

    def total_price(self):
        return int(self.product.price * self.quantity)

    def save(self,  *args, **kwargs):
        if not self._state.adding: # если мы изменяем объект
            # изменим total_price Order
            total_price = 0
            for order_item in OrderItem.objects.filter(order=self.order).exclude(id=self.id):
                total_price += int(order_item.product.price) * int(order_item.quantity)
            total_price += int(self.product.price) * int(self.quantity)
            if self.order.delivery_company == 'np': total_price += 7

            self.order.total_price = total_price
            self.order.save()

        super(OrderItem, self).save(*args, **kwargs)




class Image(models.Model):
    image = models.ImageField(max_length=300)
    product = models.ForeignKey('cosmetics.Product',null=True, blank=True, on_delete=models.CASCADE,verbose_name='Товар')  

    def save(self, *args, **kwargs):
        if self._state.adding: 
            # image_dir = self.get_img_dir(self.product.manufacturer)
            # filename = self.translate(self.product.name + '.jpg')
            image_format = self.image.name.split('.')[-1]
            image_dir = self.get_img_dir()
            filename = self.translate(str(self.image.name.split('.')[0:-1]) + '.jpg')

            image = PIL_Image.open(self.image)
            try:
                if image.mode != "RGB": image = image.convert("RGB")
            except: pass
            image_io = BytesIO()
            image.save(image_io, format='JPEG')#, quality=70

            self.image.save(f'{image_dir}/{filename}', ContentFile(image_io.getvalue()), save=False)
            
        super(Image, self).save(*args, **kwargs)
            

    def translate(self, string):
        dic = {'Ь':'', 'ь':'', 'Ъ':'', 'ъ':'', 'А':'A', 'а':'a', 'Б':'B', 'б':'b', 'В':'V', 'в':'v',
            'Г':'G', 'г':'g', 'Д':'D', 'д':'d', 'Е':'E', 'е':'e', 'Ё':'E', 'ё':'e', 'Ж':'Zh', 'ж':'zh',
            'З':'Z', 'з':'z', 'И':'I', 'и':'i', 'Й':'I', 'й':'i', 'К':'K', 'к':'k', 'Л':'L', 'л':'l',
            'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'О':'O', 'о':'o', 'П':'P', 'п':'p', 'Р':'R', 'р':'r', 
            'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'У':'U', 'у':'u', 'Ф':'F', 'ф':'f', 'Х':'Kh', 'х':'kh',
            'Ц':'Tc', 'ц':'tc', 'Ч':'Ch', 'ч':'ch', 'Ш':'Sh', 'ш':'sh', 'Щ':'Shch', 'щ':'shch', 'Ы':'Y',
            'ы':'y', 'Э':'E', 'э':'e', 'Ю':'Iu', 'ю':'iu', 'Я':'Ia', 'я':'ia'}
            
        alphabet = ['Ь', 'ь', 'Ъ', 'ъ', 'А', 'а', 'Б', 'б', 'В', 'в', 'Г', 'г', 'Д', 'д', 'Е', 'е', 'Ё', 'ё',
                    'Ж', 'ж', 'З', 'з', 'И', 'и', 'Й', 'й', 'К', 'к', 'Л', 'л', 'М', 'м', 'Н', 'н', 'О', 'о',
                    'П', 'п', 'Р', 'р', 'С', 'с', 'Т', 'т', 'У', 'у', 'Ф', 'ф', 'Х', 'х', 'Ц', 'ц', 'Ч', 'ч',
                    'Ш', 'ш', 'Щ', 'щ', 'Ы', 'ы', 'Э', 'э', 'Ю', 'ю', 'Я', 'я']
        

        st = string
        result = str()
        
        len_st = len(st)
        for i in range(0,len_st):
            if st[i] in alphabet:
                simb = dic[st[i]]
            else:
                simb = st[i]
            result = result + simb

        return result.replace(' ','_').lower()


    def get_img_dir(self):
        now = datetime.datetime.now()

        if os.path.isdir(f'media/product/{now.year}'):
            if os.path.isdir(f'media/product/{now.year}/{now.month}'):
                return str(f'media/product/{now.year}/{now.month}')
            else:
                os.mkdir(f'media/product/{now.year}/{now.month}')
                return self.get_img_dir()
        else:
            os.mkdir(f'media/product/{now.year}')
            return self.get_img_dir()

    
    class Meta:
        verbose_name_plural='4. Фотографии товаров' # verbose - подробный
        verbose_name= 'Фотография товара'
        ordering=['id']














class WhySkinBlog(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(max_length=150, unique = True,verbose_name='Ссылка', blank=True, null=True)
    content = RichTextUploadingField(verbose_name='Содержание post\'a', blank=True, null = True)
    published = models.DateTimeField(auto_now_add=True,verbose_name='Опубликовано') 
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')    
    
    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
	
    class Meta:
        verbose_name_plural='Публикации блога' # verbose - подробный
        verbose_name= 'Публикация'	
        ordering=['-published']



    def __str__(self):
        return self.title


    def save(self,  *args, **kwargs):
        if not self.pk:
            if WhySkinBlog.objects.filter(title=self.title).exists():
                self.slug = slugify(self.title) + "-" + str(uuid.uuid4())
            else:
                self.slug = slugify(self.title)
            super(WhySkinBlog, self).save(*args, **kwargs)
        else:
            super(WhySkinBlog, self).save(*args, **kwargs)
            
        try: 
            ping_google(sitemap_url='/sitemap.xml', sitemap_uses_https=True) # Вы можете захотеть «пинговать» Google, когда ваша карта сайта изменится, чтобы он знал, что нужно переиндексировать ваш сайт
        except Exception: 
            print('cannot ping Google')
            raise Exception('cannot ping Google')

    def get_absolute_url(self): # sitemap
        if get_language() == 'uk':
            return f'/blog/{self.slug}/'
        else:
            return f'/ru/blog/{self.slug}/'

