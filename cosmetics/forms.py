# Форма для создания объявлений на сайте
from email.policy import default
from django.forms import ModelForm
from django import forms
from .models import Order, Product, Image, WhySkinBlog
from django.utils.translation import gettext_lazy as _

class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields=('name', 'description', 'price', 'old_price', 'warehouse_amount', 'country', 'manufacturer', 'active_components', 'purpose', 'skin_type', 'volume', 'measure', 'status', 'how_to_use')    
        
        widgets = {
            'active_components':forms.Textarea(attrs={'placeholder':_('вводить через запятую')}),
            'description':forms.Textarea(attrs={'placeholder':_('Опишите товар как можно подробнее...')}),
            'how_to_use':forms.Textarea(attrs={'placeholder':_('Напишите, как можно использовать этот товар')}),
            'name':forms.TextInput(attrs={'placeholder':_('Название + модель')}),
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Image
        fields = ('image', )            

class OrderForm(ModelForm):
    
    class Meta:
        model = Order
        fields=('author_phone','author_name','author_surname', 'comment', 'author_email', 'way_of_payment', 'delivery_way')    
        
        widgets = {
            'author_phone':forms.TextInput(attrs={'placeholder':_('+380(__) ____-__-__')}),
            'author_email':forms.EmailInput(attrs={'placeholder':_('Введите email')}),
            'author_name':forms.TextInput(attrs={'placeholder':_('Введите имя')}),
            'author_surname':forms.TextInput(attrs={'placeholder':_('Введите фамилию')}),
            'author_patronymic':forms.TextInput(attrs={'placeholder':_('Введите отчество')}),
            'comment':forms.Textarea(attrs={'placeholder':_('Напишите, что мы должны знать об этом заказе...')}),
            'way_of_payment':forms.RadioSelect(),
            'delivery_way':forms.RadioSelect(),
        } 
        
class WhySkinBlogForm(ModelForm):
    class Meta:
        model = WhySkinBlog
        fields=('title','content')

        widgets = {
            'title':forms.TextInput(attrs={'placeholder':_('Название публикации...')}), 
            'content':forms.Textarea(attrs={'placeholder':_('Описание публикации...')}), 
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

