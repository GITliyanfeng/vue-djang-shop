from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    '''
    用户
    '''
    GENDER_CHOICES = (
        ('male', u'男'),
        ('female', u'女'),
    )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(max_length=11, verbose_name='手机号', blank=True, null=True)
    gender = models.CharField(max_length=6, verbose_name='性别', choices=GENDER_CHOICES, default='male', )
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='电子邮箱')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    '''
        储存获取到的短信验证码,用来对比验证
        可以储存在非关系型数据库中--Redis
    '''
    code = models.CharField(max_length=10, verbose_name='短信验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
