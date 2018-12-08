from django.db import models
from django.contrib.auth.models import (
        AbstractBaseUser, PermissionsMixin, BaseUserManager)
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not (telephone and username and password):
            raise ValueError('手机号，用户名和密码为必填项！')
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    uid = ShortUUIDField(primary_key=True, verbose_name='主键')
    telephone = models.CharField(
            max_length=11, unique=True, verbose_name='手机号')
    email = models.EmailField(unique=True, null=True, verbose_name='邮箱')
    username = models.CharField(max_length=30, verbose_name='用户名')
    is_active = models.BooleanField(default=True, verbose_name='是否有效账号')
    is_staff = models.BooleanField(default=False, verbose_name='是否员工账号')
    last_update = models.DateTimeField(
            auto_now=True, verbose_name='最近修改时间')
    date_joined = models.DateTimeField(
            auto_now_add=True, verbose_name='账号创建时间')

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
