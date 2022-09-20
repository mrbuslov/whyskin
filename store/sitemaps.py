from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from cosmetics.models import *
from django.db.models import Q



class ProductSitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'always'
    
    def items(self):
        return Product.objects.all()

    # def lastmod(self, obj):
    #     return obj.published
    
    
class BlogSitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'always'
    
    def items(self):
        return WhySkinBlog.objects.filter(status='published')
        

class CategorySitemap(Sitemap):
    i18n = True 
    alternates = True 
    x_default = True 
    changefreq = 'weekly'
    
    def items(self):
        return Category.objects.all()


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
                'account:profile', 'account:login', 'account:logout', 'account:registration', 'account:reset_email',
                'cosmetics:index', 'cosmetics:cart', 'cosmetics:liked', 'cosmetics:privacy_policy', 'cosmetics:contract_offer', 'cosmetics:exchange_and_return', 'cosmetics:delivery_and_payment', 'cosmetics:contacts'
            ]

    def location(self, item):
        return reverse(item)
