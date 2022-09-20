from django.contrib import admin
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.models import Group
from modeltranslation.admin import TranslationAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class ProductAdmin(TranslationAdmin): # класс-редактор представления модели
    
    change_form_template = "others/admin_product_btns.html"
    # отвечает за кнопку ОПУБЛИКОВАТЬ и переход к след.публик.
    def response_change(self, request, obj):
        if "save_btn" in request.POST:
            self.message_user(request, f'Сохранён продукт {obj.name}')
            # obj.save()
            return redirect('admin:cosmetics_product_changelist')
        elif 'save_and_new_btn' in request.POST:
            obj.save()
            return redirect('cosmetics:add_new_product')
        elif "delete_btn" in request.POST:
            next_obj = obj.pk + 1 
            obj.delete()
            self.message_user(request, f'Продукт удалён')
            if Product.objects.filter(pk = next_obj).exists():
                return redirect('admin:cosmetics_product_change', next_obj)
            else:
                return redirect('admin:cosmetics_product_changelist')
        else:
            return redirect('admin:cosmetics_product_changelist')


    list_display=('vendor_code','name', 'category', 'price', 'status')# последовательность имен полей, которые должны выводиться в списке записей
    list_display_links=('name',) # последовательность имен полей, которые должны быть преобразованы в гиперссылки, ведущие на страницу правки записи
    search_fields = ('name','vendor_code') # последовательность имен полей, по которым должна выполняться фильтрация
    prepopulated_fields = {'slug': ('name',)} # slug применяет значение title
    ordering = ['name',]
    list_filter = ('status',) # поле с фильтрами справа
    fieldsets = (
        (None, {'fields': ('image_tag', 'name', 'slug', 'description', 'category', 'price', 'old_price', 'vendor_code', 'warehouse_amount',)}),
        ('Дополнительное про товар', {'fields': ('country', 'manufacturer', 'active_components', 'purpose', 'skin_type','how_to_use')}),
        ('Другое', {'fields': ('volume', 'measure', 'status')}),
    )
    readonly_fields = ('image_tag',)
    # fields = ()

    # description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    # description_uk = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())



class ImagesFilter(admin.SimpleListFilter):
    title = 'Изображения'
    parameter_name = 'product'

    def lookups(self, request, model_admin):
        return (
            ('empty', 'empty'), # если поменять название, то меняй второй параметр
            ('full', 'full'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'empty':
            return queryset.filter(product = None)
        if self.value() == 'full':
            return queryset.exclude(product = None)


class ImageAdmin(admin.ModelAdmin): 
    list_filter = (ImagesFilter,) 


class OrderAdmin(admin.ModelAdmin):
    list_display=('order_num', 'total_price', 'author_name','author_surname', 'status')
    list_display_links=('order_num',)
    search_fields = ('order_num','author_name', 'author_surname')
    list_filter = ('status',)
    fieldsets = (
        ('Данные о товаре', {'fields': ('order_item_tag', 'order_num', 'comment', 'published', 'status', 'total_price')}),
        ('Данные о доставке и клиенте', {'fields': ('author_phone', 'author_email', 'author_name', 'author_surname', 'delivery_company', 'delivery_city', 'delivery_way', 'delivery_point')}),
    )
    readonly_fields = ('order_item_tag','published')
    

    
    change_form_template = "others/admin_order_btns.html"
    def response_change(self, request, obj):
        if "save_btn" in request.POST:
            self.message_user(request, f'Заказ сохранён')
            obj.save()
            return redirect('admin:cosmetics_order_changelist')
        elif 'submit_btn' in request.POST:
            obj.status = 'confirmed'
            # for orderitem in OrderItem.objects.filter(order=obj):
            #     if orderitem.product.warehouse_amount >= orderitem.quantity:
            #         orderitem.product.warehouse_amount -= orderitem.quantity
            #         orderitem.product.save()
            obj.save()
            return redirect('admin:cosmetics_order_changelist')
        elif 'reject_btn' in request.POST:
            obj.status = 'rejected'
            obj.save()
            return redirect('admin:cosmetics_order_changelist')
        elif "delete_btn" in request.POST:
            next_obj = obj.pk + 1 
            obj.delete()
            self.message_user(request, f'Заказ удалён')
            if Order.objects.filter(pk = next_obj).exists():
                return redirect('admin:cosmetics_order_change', next_obj)
            else:
                return redirect('admin:cosmetics_order_changelist')
        else:
            return redirect('admin:cosmetics_order_changelist')




class CategoryAdmin(TranslationAdmin): # класс-редактор представления модели
    list_display=('name',)
    list_display_links=('name',) 
    search_fields = ('name',) 
    prepopulated_fields = {'slug': ('name',)}


class WhySkinBlogAdmin(TranslationAdmin):
    list_display=('title',)
    list_display_links=('title',) 
    search_fields = ('title',) 
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(WhySkinBlog, WhySkinBlogAdmin)

admin.site.unregister(Group)