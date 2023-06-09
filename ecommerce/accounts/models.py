from django.db import models
from django.core.checks.messages import Error
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import datetime
#class MyAccountManager để quản lý các thao tác người dùng
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Địa chỉ Email là bắt buộc')

        if not username:
            raise ValueError('Tên người dùng (user name) là bắt buộc')

        # Tạo đối tượng user mới
        user = self.model(
            email=self.normalize_email(email=email),    # Chuyển email về dạng bình thường
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # requiredß
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    # Trường quyêt định khi login
    REQUIRED_FIELDS = ['username','first_name', 'last_name']   # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin    # Admin có tất cả quyền trong hệ thống

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return self.username
