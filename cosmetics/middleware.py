from django.shortcuts import redirect, render
from loguru import logger
import requests
from random import randint
import traceback

from store import settings
from django.utils.translation import gettext_lazy as _


class MyMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response
    
    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.add("logging/debug.log", format=' Time: {time}\nMsg:{message}\n', #  Filename:{file} ({file.name} --- {file.path})\n Function:{function}\n Level:{level}\n Line:{line}\n 
                    level='DEBUG', rotation='10 KB', compression='zip', ) # serialize=True
        logger.debug(exception)

        BOT_TOKEN = settings.TOKEN
        traceback_extract_tb = str(traceback.extract_tb(exception.__traceback__)[-1])
        traceback_extract_tb = traceback_extract_tb.replace('<', '').replace('>','')
        text = f'ERROR: <strong>{exception}</strong>\n\n{traceback_extract_tb}' # берём последнюю строку в ошибке ( с линией, где произошла ошибка)
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={505309520}&text={text}&parse_mode=HTML")


        quotes = [
            _('Самой большой ошибкой, которую вы можете совершить в своей жизни, является постоянная боязнь ошибаться.'),
            _('Все ошибаются. Ведь даже на карандашах есть ластики.'),
            _('Кто никогда не совершал ошибок, тот никогда не пробовал что-то новое.'),
            _('А ведь именно ошибки делают нас интересными.'),
            _('Ошибки всегда можно себе простить, если только найдется смелость признать их.'),
            _('Совершим все возможные ошибки, потому что иначе мы не узнаем, почему их не надо было делать.'),
            _('Не ошибается тот, кто ничего не делает. Не бойтесь ошибаться — бойтесь повторять ошибки.')
        ]
        authors = [
            _('Элберт Грин Хаббард'),
            _('Ленни Леонард (Симпсоны)'),
            _('Альберт Эйнштейн'),
            _('Доктор Роберт Чейз (Доктор Хаус)'),
            _('Брюс Ли'),
            _('Бернар Вербер'),
            _('Теодор Рузвельт')
        ]

        get_quote = randint(0, len(quotes)-1)

        context = {
            'quote': quotes[get_quote],
            'author': authors[get_quote]
        }

        return render(request, 'others/exception.html', context) # , context


class CartAndLiked:
    def __init__(self, get_response):
        self._get_response = get_response
    
    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_view(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.session.get('carted_prod_vend_codes', None) == None: # если сессии с покупками нет
                if request.user.carted.count() != 0: # если у пользователя есть товары в корзине на аккаунте
                    carted_prods = [str(prod.vendor_code) for prod in request.user.carted.all()]
                    request.session['carted_prod_vend_codes'] = ';'.join(carted_prods)

            if request.session.get('liked_prod_vend_codes', None) == None: 
                if request.user.liked.count() != 0: 
                    liked_prods = [str(prod.vendor_code) for prod in request.user.liked.all()]
                    request.session['liked_prod_vend_codes'] = ';'.join(liked_prods)

    def set_session_when_login(self, *args):
        args = args[0]
        request = self._get_response
        if args['author_name'] and args['author_name'] != '':
            request.session['author_name'] = args['author_name']
            if request.user.first_name == '' or request.user.first_name == None: 
                request.user.first_name = args['author_name']
                request.user.save()
        elif args['author_name'] == None:
            request.session['author_name'] = request.user.first_name

        if args['author_surname'] and args['author_surname'] != '':
            request.session['author_surname'] = args['author_surname']
            if request.user.last_name == '' or request.user.last_name == None: 
                request.user.last_name = args['author_surname']
                request.user.save()
        elif args['author_surname'] == None:
            request.session['author_surname'] = request.user.last_name

        if args['author_phone'] and args['author_phone'] != '':
            request.session['author_phone'] = args['author_phone']
            if request.user.phone_number == '' or request.user.phone_number == None: 
                request.user.phone_number = args['author_phone']
                request.user.save()
        elif args['author_phone'] == None:
            request.session['author_phone'] = request.user.phone_number
            
        if args['author_email'] and args['author_email'] != '':
            request.session['author_email'] = args['author_email']
            if request.user.email == '' or request.user.email == None: 
                request.user.email = args['author_email']
                request.user.save()
        elif args['author_email'] == None:
            request.session['author_email'] = request.user.email


