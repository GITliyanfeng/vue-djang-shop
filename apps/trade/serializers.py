# -*- coding: utf-8 -*-
# __author__ : py_lee
# __time__   : '18-12-17 上午10:31'
import time
from random import randint

from rest_framework import serializers

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializer import GoodsSerializer
from utils.aliypay import AliPay
from DjangoVue.settings import rsa_aliy_key_path, rsa_private_key_path,APP_ID,app_notify_url,return_url


class ShoppingCareSerializers(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, label='商品购买数量', error_messages={
        'min_value': '商品数量不能小于1',
        'require': '请选择购买数量',
    }, help_text='商品数量')
    goods = serializers.PrimaryKeyRelatedField(required=True, label='商品', queryset=Goods.objects.all(),
                                               help_text='商品ID')

    def create(self, validated_data):
        # serializers.Serializer中将请求上下问放到了self.context中,
        # serializers.ModelSerializer中,将请求上下文放到了self中
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        # 查看数据库中是否存在这一条记录
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        # 修改商品的数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class ShoppingCartDetialSerializers(serializers.ModelSerializer):
    # 外键,一个人购物车的记录对应一种商品
    goods = GoodsSerializer(many=False, )

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class OrderInfoSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    # 可定制的Serializer字段,自由度高,而且不依赖于Model中的字段,这个字段是用来生成支付页面的url的,只能被访问,不能被更改,所以是只读的
    alipay_url = serializers.SerializerMethodField(read_only=True)

    # 对应SerializerMethodField可定制字段的方法get_xxx,固定的写法
    def get_alipay_url(self, obj):
        alipay = AliPay(
            # appid在沙箱环境中就可以找到
            appid=APP_ID,
            # 这个值先不管，在与vue的联调中介绍
            app_notify_url=app_notify_url,
            # 我们自己商户的密钥
            app_private_key_path=rsa_private_key_path,
            alipay_public_key_path=rsa_aliy_key_path,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,

            # 先不用管，后面vue解释
            return_url=return_url
        )
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.order_mount,
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        # 这样就实现了将支付宝支付界面的url序列化到Serializer中
        return re_url

    def generate_order_sn(self):
        # 当前时间+user_id+随机数
        timestr = time.strftime("%Y%m%d%H%M%S")
        user_id = self.context['request'].user.id
        randomstr = randint(10, 99)
        order_sn = "{timestr}{user_id}{randomstr}".format(timestr=timestr, user_id=user_id, randomstr=randomstr)
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializers(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetaileSerializers(serializers.ModelSerializer):
    goods = OrderGoodsSerializers(many=True)
    # 可定制的Serializer字段,自由度高,而且不依赖于Model中的字段,这个字段是用来生成支付页面的url的,只能被访问,不能被更改,所以是只读的
    alipay_url = serializers.SerializerMethodField(read_only=True)

    # 对应SerializerMethodField可定制字段的方法get_xxx,固定的写法
    # 在订单详情中也有支付宝支付的接口
    def get_alipay_url(self, obj):
        alipay = AliPay(
            # appid在沙箱环境中就可以找到
            appid=APP_ID,
            # 这个值先不管，在与vue的联调中介绍
            app_notify_url=app_notify_url,
            # 我们自己商户的密钥
            app_private_key_path=rsa_private_key_path,
            alipay_public_key_path=rsa_aliy_key_path,
            # debug为true时使用沙箱的url。如果不是用正式环境的url
            debug=True,  # 默认False,

            # 先不用管，后面vue解释
            return_url=return_url
        )
        url = alipay.direct_pay(
            # 订单标题
            subject=obj.order_sn,
            # 我们商户自行生成的订单号
            out_trade_no=obj.order_sn,
            # 订单金额
            total_amount=obj.order_mount,
        )
        # 将生成的请求字符串拿到我们的url中进行拼接
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        # 这样就实现了将支付宝支付界面的url序列化到Serializer中
        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'
