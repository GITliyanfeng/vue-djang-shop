from django.shortcuts import render, redirect
from datetime import datetime

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from utils.permissions import IsOwnerOrReadOnly
from trade.serializers import ShoppingCareSerializers, ShoppingCartDetialSerializers, OrderInfoSerializers, \
    OrderDetaileSerializers
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from utils.aliypay import AliPay
from DjangoVue.settings import rsa_aliy_key_path, rsa_private_key_path, APP_ID, app_notify_url, return_url


# Create your views here.

class ShoppingCarViewSets(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        列出购物车内的记录
    create:
        商品添加到购物车
    delete:
        删除购物车中的记录
    update:
        更新购物车信息
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCareSerializers
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    # 购物车引起商品库存的变化
    # 新增商品到购物车
    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.goods_num -= instance.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods = instance.goods
        goods.goods_num -= instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        # 定义更改数据的时候的额外逻辑
        # 逻辑:记录更改前后的数据,比较大小来分支不同的操作
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        update_record = serializer.save()
        update_nums = update_record.nums
        nums = existed_nums - update_nums
        goods = update_record.goods
        goods.goods_num += nums
        goods.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetialSerializers
        else:
            return ShoppingCareSerializers


class OrderViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    create:
        创建一个订单
    list:
        查看用户订单列表
    delete:
        取消订单

    """
    # 权限
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # 认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetaileSerializers
        else:
            return OrderInfoSerializers

    def perform_create(self, serializer):
        # 在保存之前和保存之后都需要添加自己的逻辑
        # 保存之前,生成订单号,在serializer中进行
        order = serializer.save()
        # 获取 购物车中的商品
        shopcart = ShoppingCart.objects.filter(user=self.request.user)
        # 将购物车中的商品,添加到OrderGoods表中
        for shop_cart in shopcart:
            ordergood = OrderGoods()
            ordergood.goods = shop_cart.goods
            ordergood.nums = shop_cart.nums
            ordergood.order = order
            ordergood.save()
            # 将购物车中的记录删除掉
            shop_cart.delete()
        return order


from rest_framework.views import APIView


# 关于支付宝支付,没有model所以直接使用底层的APIView
class AliPayView(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        process_dic = {}
        for k, v in request.GET.items():
            process_dic[k] = v
        sign = process_dic.pop('sign', None)
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
            return_url=app_notify_url
        )
        verify_res = alipay.verify(process_dic, sign)

        # 当支付被验证成功
        if verify_res:
            # return Response("success")
            response = redirect('index')
            # 设置重定向到首页,然后在cookies中设置nextpath,前端js来执行跳转到pay
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            # 失败的话不跳转到pay,而是直接跳转到首页
            response = redirect('index')
            return response

    def post(self, request):
        """
        处理支付宝的notify_url的返回
        :param request:
        :return:
        """
        process_dic = {}
        for k, v in request.POST.items():
            process_dic[k] = v
        sign = process_dic.pop('sign', None)
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
        verify_res = alipay.verify(process_dic, sign)

        if verify_res:
            order_sn = process_dic.get("out_trade_no", None)
            trade_no = process_dic.get('trade_no', None)
            trade_status = process_dic.get('trade_status', None)
            exist_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exist_order in exist_orders:
                # 支付成功之后,修改商品的销量
                order_goods = exist_order.goods.all()
                for order_good in order_goods:
                    good = order_good.goods
                    good.sold_num += order_good.nums
                    good.save()
                # 支付成功后修改订单的支付信息,状态
                exist_order.trade_no = trade_no
                exist_order.pay_status = trade_status
                exist_order.pay_time = datetime.now()
                exist_order.save()

            return Response("success")

