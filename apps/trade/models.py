from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods

User = get_user_model()


# Create your models here.

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name='用户', help_text='用户ID')
    goods = models.ForeignKey(Goods, verbose_name='商品', help_text='商品ID')
    nums = models.IntegerField(default=0, verbose_name='购买数量', help_text='购买数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        # 用户和商品要构成联合唯一索引
        unique_together = ('user', 'goods')

    def __str__(self):
        return "商品:{}({})件".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ('WAIT_BUYER_PAY', '交易创建，等待买家付款'),
        ('TRADE_CLOSED', '未付款交易超时关闭，或支付完成后全额退款'),
        ('TRADE_SUCCESS', '交易支付成功'),
        ('TRADE_FINISHED', '交易结束，不可退款'),
        ('paying', '待支付'),
    )
    user = models.ForeignKey(User, verbose_name='用户')
    order_sn = models.CharField(unique=True, max_length=30, verbose_name='订单号', blank=True, null=True)
    # nonce_str = models.CharField(max_length=50, null=True, blank=True, verbose_name='随机码')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付宝单号')
    pay_status = models.CharField(max_length=20, choices=ORDER_STATUS, verbose_name='订单状态', default='paying')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    post_script = models.CharField(max_length=200, verbose_name='订单留言')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 用户信息
    address = models.CharField(max_length=100, default="", verbose_name='收货地址', )
    signer_name = models.CharField(max_length=20, default="", verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, verbose_name='联系电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    order = models.ForeignKey(OrderInfo, verbose_name='订单信息', related_name='goods')
    goods = models.ForeignKey(Goods, verbose_name='商品')
    nums = models.IntegerField(default=0, verbose_name='购买数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
