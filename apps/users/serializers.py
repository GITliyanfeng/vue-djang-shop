# -*- coding: utf-8 -*-
# __author__ : py_lee
# __time__   : '18-12-13 下午6:22'
import re
from datetime import datetime, timedelta

from django.contrib.auth.backends import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from DjangoVue.settings import MOBILE_REGSTER
from users.models import VerifyCode

User = get_user_model()


class UserRegsterSerializers(serializers.ModelSerializer):
    """
    使用modelSerializer可以带来便利,但是它会对字段进行限制,默认只能使用
    定义的model中提供的字段,不能多不能少,这里前端页面会提交过来一个code字段
    ,这个字段是model中没有定义的字段,所以需要突破这个限制
    """
    code = serializers.CharField(max_length=4, min_length=4, required=True, help_text='手机验证码', label="验证码",
                                 write_only=True,
                                 error_messages={
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误',
                                     'blank': '验证码不能为空',
                                 })
    # 额外的对username的验证
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        label="用户名",
        # 使用UniqueValidator来验证User表中的username的唯一性
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
    )
    # 密码
    password = serializers.CharField(
        required=True,
        allow_null=False,
        write_only=True,
        label='密码',
        style={
            'input_type': 'password',
        }
    )

    # 重写code字段的验证方法,自己制定验证规则
    def validate_code(self, code):
        # 不使用get的方式,是因为要处理获取不到和获取到多个相同的这两个异常
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data['username'],code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass
        # 验证码是否存在?initial_data中是前端传送过来的数据[未验证]
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_verify_record = verify_records[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            # 如果最新一条记录的时间>(当前时间-5min)意味着那一条记录已经过期了
            if five_minute_ago > last_verify_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if not last_verify_record.code == code:
                raise serializers.ValidationError('验证码有误')
        else:
            raise serializers.ValidationError('验证码有误')

    # 重写,除了code字段之外的其他字段的验证方式
    def validate(self, attrs):
        # 由于前端是用手机号进行注册,而且字段填写的是username字段,所以这里我们需要自行填充mobile字段
        attrs['mobile'] = attrs['username']
        # 因为model中并没定义code字段,所以需要将前端传递过来的多余的字段删除掉,否则默认的验证方式会出现问题
        del attrs['code']
        # 将处理过的字段返回
        return attrs  # 现在这个里边有username,mobile,password

    # 传统的方式通过重写create完成密码保存
    # 重写create方法,因为create方法默认将验证之后的结果填充到数据库,像密码这种字段需要使用加密的算法加密之后才可以储存
    # 所以需要添加自己的逻辑
    """
    def create(self, validated_data):
        # 首先继承父类的create方法,然后在结果上进行修改
        user = super(UserRegsterSerializers, self).create(validated_data=validated_data)
        # 因为UserProfile继承AbstractUser,有set_password方法,所以这里可以直接使用
        user.set_password(validated_data['password'])
        user.save()
        return user
    """

    # 当我们retrieve用户详情的时候,会发现只返回了username和mobile,然而我们需要的不仅仅是这些
    # 之所以只是返回这两个信息,使用为上面的定义中,我们只定义了这两个字段是只读可访问的
    # 所以我们不能直接来获取用户详情,需要动态的去设置可读字段

    class Meta:
        model = User
        fields = ('username', 'mobile', 'code', 'password')


# 当获取用户详情的时候,从viewset中设置动态设置UserDetialSerializers来做序列化
class UserDetialSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'birthday', 'mobile', 'gender', 'email')


class SmsCodeSerializers(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, required=True)

    def validate_mobile(self, mobile):
        """
        自定义对输入的手机号码进行验证
        :param mobile:
        :return:
        """
        # 验证手机号码是否合法
        mobile_reg = re.compile(MOBILE_REGSTER)
        if not mobile_reg.match(string=mobile):
            raise serializers.ValidationError('当前手机号码不合法')
        # 手机是否已经被注册
        elif User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('当前手机号已经被注册')
        # 验证发送频率
        # 定义发送时间的flag
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(mobile=mobile, add_time__gt=one_minute_ago).count():
            raise serializers.ValidationError('发送频率过高,一分钟后重试')
        return mobile
