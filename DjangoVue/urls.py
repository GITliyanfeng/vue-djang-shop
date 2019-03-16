"""DjangoVue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
# from django.contrib import admin
import xadmin

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token

from DjangoVue.settings import MEDIA_ROOT
from django.views.static import serve
# viewset
from goods.views import GoodsListViewSet, GoodsCategoryViewSet, HotSearchsViewset, BannerViewSet, IndexCategoryViewSet
from user_operation.views import UserFavViewSet, LeaveMessageViewSet, AddressViewSet
from users.views import SmsCodeViewSet, UserViewSet
from trade.views import ShoppingCarViewSets, OrderViewSet
from trade.views import AliPayView
#############-------router配置--------##############
# router
from rest_framework.routers import DefaultRouter

# 实例化router并对router配置
router = DefaultRouter()
# 将goods对应的viewset注册入router的urls中,使router分配接口路由
router.register(r'goods', GoodsListViewSet, basename='goods')
router.register(r'categorys', GoodsCategoryViewSet, basename='categorys')
router.register(r'code', SmsCodeViewSet, basename='smscode')
# 热搜词
router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")
# 用户收藏功能
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")
# 用户注册
router.register(r'users', UserViewSet, base_name="user")
# 用户留言功能
router.register(r'messages', LeaveMessageViewSet, base_name="messages")
# 用户配送地址管理功能
router.register(r'address', AddressViewSet, base_name="address")
# 用户购物车接口
router.register(r'shopcarts', ShoppingCarViewSets, base_name="shopcarts")
# 订单相关的接口
router.register(r'orders', OrderViewSet, base_name="orders")
# 首页轮播图相关接口
router.register(r'banners', BannerViewSet, base_name="banners")
# 首页商品商标系列数据
router.register(r'indexgoods', IndexCategoryViewSet, base_name="indexgoods")

# 以后只要将接口的路由和访问数据的viewset注册入router就可以了,下面的 urlpatterns 就不用在多余的配置了

##################---------#############################
# 引入文档
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url(r'^admin/', include(xadmin.site.urls)),
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # 开始配置路由
    # 文档路由 --- 一定不可以携带终止$符号
    url(r'^docs/', include_docs_urls(title='文档')),
    # 商品列表
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 富文本编辑器
    url(r'ckeidtor/', include('ckeditor_uploader.urls', )),
    # 配置token认证的url
    url(r'^api-token-auth/', obtain_auth_token),
    # 配合jwt的认证 -- y由于要使适应前端的接口  改为login/
    # url(r'^api-token-jwt-auth/', obtain_jwt_token),
    url(r'^login/', obtain_jwt_token),
    # 支付宝支付url
    url(r'^alipay/return/', AliPayView.as_view(), name='alipayz'),
    # 主页url
    url(r'^index/', TemplateView.as_view(template_name='index.html'), name='index'),
]
