from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from .sitemaps import * # Sitemap
from django.contrib.sitemaps.views import sitemap, index 
from . import settings
from django.utils.translation import gettext_lazy as _


sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blog': BlogSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
]
if 'rosetta' in settings.INSTALLED_APPS: # это графический редактор переведённого текста
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]

urlpatterns += i18n_patterns (
    path('only_for_admin/', admin.site.urls),
    # https://www.websiteplanet.com/ru/webtools/sitemap-validator/
    
    path('sitemap.xml', index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ckeditor',include('ckeditor_uploader.urls')),
    # path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    
    path('',include('account.urls', namespace='account')),
    path('', include('cosmetics.urls', namespace='cosmetics')),

    prefix_default_language=False, # чтобы не было /uk/ в строке

)


admin.site.index_title = "WhySkin"
admin.site.site_header = "WhySkin Admin"
admin.site.site_title = "Admin"

# errors handlers
# handler400 = 'cosmetics.views.handler400_error' # неверный запрос
handler403 = 'cosmetics.views.handler403_error' # запрещён доступ к странице
handler404 = 'cosmetics.views.handler404_error' # неверная страница
handler500 = 'cosmetics.views.handler500_error' # проблема с сервером