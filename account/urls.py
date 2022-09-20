from django.urls import path
from account import views as account_views
from django.contrib.auth import views as auth_views


app_name='account'

urlpatterns = [
    path('profile/', account_views.profile, name='profile'),
    path('login/', account_views.user_login ,name='login'),
    path('logout/', account_views.user_logout, name='logout'),
    path('registration/', account_views.registration, name='registration'),
    path('set_new_pswrd/<uidb64>/<token>', account_views.SetNewPswrdView.as_view(), name = 'set_new_pswrd'),
    path('reset_email/', account_views.RequestResetEmailView.as_view(), name = 'reset_email'),
]