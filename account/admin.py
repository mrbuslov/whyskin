from django.contrib import admin

from django.contrib import admin
from account.models import Account
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect

class HidePassword(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('password',)




class AccountAdmin(UserAdmin): 
    form = HidePassword # скрываем пароль

    list_display = ('email',)
    search_fields = ('email',)
    ordering=('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'phone_number', 'first_name', 'last_name')}),
        ('Личная информация', {'fields': ( 'unique_code', 'telegram','chat_id', 'date_joined','last_login')}),
        ('Разрешения', {'fields': ('is_admin','is_active', 'is_blocked', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Другое', {'fields': ('liked', 'carted')}),
    )
    
    readonly_fields = ( 'unique_code', 'chat_id', 'date_joined','last_login')

    class Meta:
        model = Account




admin.site.register(Account, AccountAdmin)