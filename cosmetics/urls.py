from django.shortcuts import render
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name='cosmetics'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('category/<str:category>/', views.category, name='category'),
    path('product/<str:product>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('liked/', views.liked, name='liked'),
    path('order/', views.order, name='order'),
    path('order_success/', views.order_success, name='order_success'),

    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('contract_offer/', views.contract_offer, name='contract_offer'),
    path('exchange_and_return/', views.exchange_and_return, name='exchange_and_return'),
    path('delivery_and_payment/', views.delivery_and_payment, name='delivery_and_payment'),
    path('contacts/', views.contacts, name='contacts'),

    path('my_admin/', views.my_admin, name='my_admin'),
    path('add_new_product/', views.add_new_product, name='add_new_product'),
    path('all_products_admin/', views.all_products_admin, name='all_products_admin'),
    
    path('blog/<str:slug>/', views.blog_post, name='blog_post'),
    path('add_blog_post/', views.add_blog_post, name='add_blog_post'),
    path('blog/', views.blog, name='blog'),

    path('error/', views.error, name='error'),

]