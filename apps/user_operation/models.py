from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model()


# Create your models here.

class UserFav(models.Model):
    """
    用户的收藏
    """
    user = models.ForeignKey(User, verbose_name='用户', help_text='用户的ID号')
    goods = models.ForeignKey(Goods, verbose_name='商品', help_text='商品的ID号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        # 将user和goods两个元素联合唯一操作  两者共同建立了一个唯一索引---针对的是数据库
        unique_together = ('user', 'goods',)

    def __str__(self):
        return self.user.username


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购'),
    )
    user = models.ForeignKey(User, verbose_name='用户', help_text='用户的ID')
    message_type = models.IntegerField(choices=MESSAGE_CHOICES, default=1, verbose_name='留言类型',
                                       help_text='留言类型:1-留言,2-投诉,3-询问,4-售后,5-求购')
    subject = models.CharField(max_length=100, default="", verbose_name='留言主题', help_text='留言主题')
    message = models.TextField(default="", verbose_name='留言内容', help_text='留言内容')
    file = models.FileField(upload_to="message", verbose_name='上传的文件', help_text='上传的文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name='用户')
    province = models.CharField(max_length=100, default='', verbose_name='省份', help_text='省份')
    city = models.CharField(max_length=100, default='', verbose_name='城市', help_text='城市')
    district = models.CharField(max_length=100, default="", verbose_name='区域', help_text='区域')
    address = models.CharField(max_length=100, default="", verbose_name='详细地址', help_text='详细地址')
    signer_name = models.CharField(max_length=100, default="", verbose_name='签收人', help_text='签收人姓名')
    signer_mobile = models.CharField(max_length=11, default="", verbose_name='签收人', help_text='签收人手机号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
