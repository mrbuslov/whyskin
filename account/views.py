import imp
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from account.forms import ProfileEditForm
from cosmetics.middleware import CartAndLiked

from .models import Account
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse, reverse_lazy
from .utils import token_generator
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
import threading
from django.views.generic import View
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Q
import re
from django.utils.translation import get_language

def user_login(request):
    if request.user.is_authenticated:
        return redirect('cosmetics:index')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                # email
                user = authenticate(email=email, password=password)
            except:
                # номер телефона
                user = authenticate(email=Account.objects.get(phone_number=email).email, password=password)
                
            # когда мы логинимся, сессия сбрасывается. Синхронизируем данные пользователя
            user_data = {
                'author_name': request.session.get('author_name', None),
                'author_surname': request.session.get('author_surname', None),
                'author_phone': request.session.get('author_phone', None),
                'author_email': request.session.get('author_email', None),
            }
            if user is not None:
                login(request, user)
                CartAndLiked(request).set_session_when_login(user_data)
                if 'next' in request.POST: return redirect(request.POST.get('next'))
                return redirect('account:profile')
            else:  
                return render(request, 'account/login.html')
        else:  
            return render(request, 'account/login.html')

def user_logout(request):
    logout(request)
    return redirect('cosmetics:index')



def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Account.objects.filter(email=email).exists():
            try: user = authenticate(email=email, password=password)
            except: pass                

            if user is not None:
                login(request, user)
                if 'next' in request.POST: return redirect(request.POST.get('next'))
                return redirect('cosmetics:profile')


        user = Account.objects.create_user(password=password, email=email.lower())
        user.save()
        
        mail_title = "Дякуємо за реєстрацію на WhySkin!"
        html = get_template('email/registration.html')
        text = f'WhySkin (https://whyskin.com.ua/) Дякуємо за реєстрацію на WhySkin! Відтепер ми швидше оформлятимемо Вам замовлення!😊 Виникли додаткові запитання? Наші контакти: Номер телефону: +380(98) 622-50-33 (tel:+380986225033) Телеграм: @whyskin (https://t.me/whyskin) WhySkin - магазин корейської косметики з індивідуальним підходом❤️ Завжди свіжі новинки для всіх типів шкіри!'

        msg = EmailMultiAlternatives(
            mail_title,
            text,
            settings.EMAIL_HOST_USER,
            [email])
        msg.attach_alternative(html, "text/html")
        EmailThreading(msg).start() # мы быстрее отправляем email

        return render(request, 'account/registration_success.html', {'email':email})

    else:
        return render(request, 'account/registration.html')



# view для того, чтобы быстрее отправлять email
class EmailThreading(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'account/reset_email.html')
    
    def post(self, request):
        email = request.POST.get('email', None)
        
        if email is None or not Account.objects.filter(email=email).exists():
            return render(request, 'account/reset_email.html')

        user = Account.objects.filter(email=email)
        if user.exists():
            uidb64 =urlsafe_base64_encode(force_bytes(user[0].pk))

            domain = get_current_site(request).domain
            link = reverse('account:set_new_pswrd', kwargs={'uidb64':uidb64,'token':token_generator.make_token(user[0])})

            renew_password_url='http://' + domain + link

            mail_title = "Оновлення пароля"
            variables = {
                'activate_url': renew_password_url,
            }
            html = get_template('email/email_reset_password.html').render(variables)
            text = f'WhySkin (https://whyskin.com.ua/) Забули пароль?\nЩоб скинути пароль, натисніть кнопку нижче.\nСкинути пароль\n{renew_password_url}\nЯкщо Ви не бажаєте змінювати свій пароль або не запитували скидання паролю, Ви можете проігнорувати або видалити цей лист.\nWhySkin - магазин корейської косметики з індивідуальним підходом❤️\nЗавжди свіжі новинки для всіх типів шкіри!'
            
            msg = EmailMultiAlternatives(
                mail_title,
                text,
                settings.EMAIL_HOST_USER,
                [email])
            msg.attach_alternative(html, "text/html")
            EmailThreading(msg).start() # мы быстрее отправляем email

            return render(request, 'account/reset_email_success.html')
        else:
            return redirect('account:registration')

class SetNewPswrdView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=user_id)

            if PasswordResetTokenGenerator().check_token(user, token):
                return render(request, 'account/reset_email.html') # Пароль кликают 2-ой раз, так нельзя. Отошлём на повторную отправку
        except DjangoUnicodeDecodeError as identifier:
            return render(request, 'account/reset_email.html')
        return render(request, 'account/set_new_pswrd.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
            
        }

        password = request.POST.get('password', None)
        if password is None or len(password) < 4 or len(password) > 20:
            return render(request, 'account/set_new_pswrd.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = Account.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            return redirect('/login/')
        except DjangoUnicodeDecodeError as identifier:
            return render(request, 'account/set_new_pswrd.html', context)


@login_required(login_url='/login/')
def profile(request):
    account = Account.objects.get(pk=request.user.pk) 
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=account)
        if form.is_valid():
            post = form.save(commit=False)    
            # if post.phone_number == None or not re.match(r'^\+?3?8?(0\d{9})$', post.phone_number):
            #     return redirect('account:profile')
            post.save()
        return redirect('account:profile')

    
    form = ProfileEditForm(instance=account)
    return render(request, 'account/profile.html', {'form':form, 'account':account,})
    
