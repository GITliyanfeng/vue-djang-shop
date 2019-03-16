# -*- coding: utf-8 -*-
# __author__ : py_lee
# __time__   : '18-12-14 下午2:54'
import re
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from goods.serializer import UserFavGoodsSerializers
from DjangoVue.settings import MOBILE_REGSTER


class UserFavSerializers(serializers.ModelSerializer):
    # 自定义user字段,是个隐藏域,默认获取的是当前登录状态的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # 上面创建了唯一索引，所以重复添加会报错，因此可以自定义错误信息,由于是modelserialzer可以自动识别
        # model表中创建的unique_together,也就是说会有默认的异常信息,但是我们也可以自定义
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='不可以重复收藏',
            ),
        ]

        model = UserFav
        # 这里添加是为了后期取消收藏的时候可以找到商品
        fields = ('user', 'goods', 'id')


class UserFavDetialSerializers(serializers.ModelSerializer):
    """
    用户收藏的详情
    为了能获取用户收藏的商品的详细信息,所以需要将GoodsSerializers进行嵌套
    """
    goods = UserFavGoodsSerializers()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class LeaveMessageSerializers(serializers.ModelSerializer):
    """
    用户留言相关的Serializer
    """
    # 自定义user字段,是个隐藏域,默认获取的是当前登录状态的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message_type', 'subject', 'message', 'file', 'add_time')


class AddressSerializers(serializers.ModelSerializer):
    """
    用户收货地址相关的Serializer
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    province = serializers.CharField(max_length=100, required=True, allow_null=False, label='省份', error_messages={
        'max_length': '格式有误',
        'required': '省份必填'
    })
    city = serializers.CharField(max_length=100, required=True, allow_null=False, label='城市', error_messages={
        'max_length': '格式有误',
        'required': '城市必填'
    })
    district = serializers.CharField(max_length=100, required=True, allow_null=False, label='区域', error_messages={
        'max_length': '格式有误',
        'required': '区域必填'
    })
    address = serializers.CharField(max_length=100, required=True, allow_null=False, label='详细地址', error_messages={
        'max_length': '格式有误',
        'required': '详细地址必填'
    })

    signer_name = serializers.CharField(max_length=100, required=True, allow_null=False, label='收件人', error_messages={
        'required': '必须填写姓名'
    })
    signer_mobile = serializers.CharField(max_length=11, min_length=11, required=True, label='收件人手机号', allow_null=False)

    def validate_signer_mobile(self, signer_mobile):
        mobile_reg = re.compile(MOBILE_REGSTER)
        if not mobile_reg.match(string=signer_mobile):
            raise serializers.ValidationError('当前手机号码不合法')
        return signer_mobile

    class Meta:
        model = UserAddress
        fields = '__all__'
