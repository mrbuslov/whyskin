from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.contrib.auth.models import PermissionsMixin

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Введите email')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	phone_number			= models.CharField(max_length=13, verbose_name='Номер телефона', blank=True, unique=True, null=True)
	first_name				= models.CharField(max_length=30, default='', blank=True, verbose_name='Имя')
	last_name				= models.CharField(max_length=30, default='', blank=True, verbose_name='Фамилия')

	telegram = models.BooleanField(null=True, default=False, verbose_name='Telegram')
	chat_id = models.BigIntegerField(null=True, blank=True, verbose_name='chat id', editable=False)

	date_joined				= models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='Последний вход', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	is_blocked				= models.BooleanField(default=False)
	unique_code				= models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

	liked = models.ManyToManyField('cosmetics.Product', related_name="liked", default=None, blank=True, verbose_name = "Понравившиеся товары")
	carted = models.ManyToManyField('cosmetics.Product', related_name="carted", default=None, blank=True, verbose_name = "Товары в корзине")

	USERNAME_FIELD = 'email'
	objects = MyAccountManager()

	
	class Meta:
		verbose_name_plural='Профили пользователей' # verbose - подробный
		verbose_name= 'Профиль пользователя'
		ordering=['email']

	def __str__(self):
		return self.email
	
	def get_first_part_email(self): # использовано в base.html
		return self.email.split('@')[0]