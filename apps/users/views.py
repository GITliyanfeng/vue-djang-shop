from django.shortcuts import render
# Create your views here.
# 定义用户登录的认证方式
from random import choice
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.serializers import SmsCodeSerializers, UserRegsterSerializers, UserDetialSerializers
from utils.send_sms import YunPian
from DjangoVue.settings import API_KEY
from users.models import VerifyCode

# 获取当前使用的user模型
User = get_user_model()


class CoustomBankends(ModelBackend):
    """
    自定义用户登录方式
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    create:
        用户注册
    """
    serializer_class = UserRegsterSerializers
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    # 权限问题,如果直接使用permission_classes = (IsAuthenticated,)那么用户注册的create方法会出现问题,所以需要动态的
    # 去添加权限,重写[APIView的]get_prrmissions方法
    def get_permissions(self):
        # 通过判断行为去添加权限,注意返回的是数组,而且内部元素需要手动加括号实例化
        if self.action == 'retrieve':
            return [IsAuthenticated(), ]
        elif self.action == 'create':
            return []
        return []

    # 场景,用户注册完成之后,自动登录,所以需要重载create方法,将用户的token返回,因为默认没有返回token的接口的
    # 重载的来源是mixins.CreateModelMixin,直接将create方法内的所有复制过来,再改改添加我们需要的功能
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 在这根据user生成JWT的tokne,但是用户对象在perform_create函数中,它并没有返回给当前函数,所以
        # 还需要重写perform_create,使它可以返回用户对象
        user = self.perform_create(serializer)
        # 获取到用户对象后,手动生成JWT-token
        res_dic = serializer.data
        payload = jwt_payload_handler(user)
        # 将生成的token放到serializer.data中
        res_dic['token'] = jwt_encode_handler(payload)
        # 当然也可以添加其他信息,假如前端需要的话
        res_dic['name'] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(res_dic, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        # 因为create方法并没有返回用户的id,所以没办法组合成为完整的uri去请求一个用户详情,所以
        # 这里重写get_object方法,去获取用户的详情,直接返回当前用户
        # 注意get_object方法不仅仅会影响到mixins.RetrieveModelMixin还会影响到, mixins.DestroyModelMixin
        return self.request.user

    def perform_create(self, serializer):
        # 它只是做了save,而没有返回user对象
        # serializer.save()
        user = serializer.save()
        return user

    # 重载get_serializer_class函数来动态的使用serializer
    def get_serializer_class(self):
        # 通过判断行为去动态设置serializers
        if self.action == 'retrieve':
            return UserDetialSerializers
        elif self.action == 'create':
            return UserRegsterSerializers
        return UserDetialSerializers


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    # 需要验证的逻辑 : 1.当前手机号是否合法,2.当前手机号是否已经被注册
    serializer_class = SmsCodeSerializers

    def generic_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = '1234567890'
        random_str_list = [choice(seeds) for i in range(4)]
        return ''.join(random_str_list)

    # 重写create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取手机号
        mobile = serializer.validated_data['mobile']
        # 请求验证码
        code = self.generic_code()
        yun_pian = YunPian(api_key=API_KEY)
        # sms_status = yun_pian.send_sms(mobile=mobile, code=code)
        sms_status = yun_pian.send_test(mobile=mobile, code=code)
        if not sms_status['code'] == 0:
            return Response({'mobile': sms_status['msg']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 当短信发送成功的时候,数据库保存验证码
            code_record = VerifyCode(mobile=mobile, code=code)
            code_record.save()
            return Response({'mobile': mobile, 'sms': sms_status['sms']}, status=status.HTTP_201_CREATED)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
