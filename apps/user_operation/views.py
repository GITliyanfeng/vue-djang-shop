from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
# 单独配置jwt权限认证
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from user_operation.serializers import UserFavSerializers, UserFavDetialSerializers, LeaveMessageSerializers, \
    AddressSerializers
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        列出当前用户的所有收藏
    retrieve:
        获取某个收藏
    create:
        添加一个收藏
    destroy:
        删除一个收藏
    """
    # 权限认证  首先认证是否登录,其次认证是否是资源的拥有者
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 第一个登录认证是JWT认证,第二个认证是Session认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 设置用于搜索的字段,默认是pk也就是主键(ID)可以自定义,这里我将goods的id作为搜索字段,也就是.../userfavs/"lookup_field"
    # 注意:lookup_fiel是在get_queryset的结果中做检索的,不用担心是在all中做检索
    lookup_field = 'goods_id'

    # 重写get_queryset方法,用户中能获取用户自己的收藏列表
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetialSerializers
        elif self.action == 'create':
            return UserFavSerializers
        return UserFavSerializers


class LeaveMessageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    用户的留言功能
    list:
        获取当前用户的留言列表
    create:
        用户添加留言
    delete:
        删除留言
    """
    # 权限
    serializer_class = LeaveMessageSerializers
    # 身份验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user).order_by('-add_time')


# 增删改查都涉及到的,直接使用viewsets.ModelViewSet
class AddressViewSet(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取用户收货地址的列表
    create:
        添加收货地址
    delete:
        删除收货地址
    update:
        修改收货地址
    """
    # 权限
    serializer_class = AddressSerializers
    # 身份验证
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).order_by('-add_time')
