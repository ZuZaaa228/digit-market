from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('У тебя че почты нет? Введи да')
        if not username:
            raise ValueError('Ты бы еще номер свой ввел, дай имя')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def buy_tank(self, tank_sale):
        if self.balance >= tank_sale.price:
            self.balance -= tank_sale.price
            self.save()
            tank_sale.buyer = self
            tank_sale.save()
            tank_sale.tank.owner = self
            tank_sale.tank.is_for_sale = False
            tank_sale.tank.save()
            return True
        else:
            return False
