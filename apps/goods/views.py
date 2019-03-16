############
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
#################
from goods.serializer import GoodsSerializer, GoodsCategorySerializer, HotWordsSerializer, BannerSerializers, \
    IndexCategorySerializer
from goods.models import Goods, GoodsCategory, HotSearchWords, Banner
from goods.pagination import GoodsSetPagination
################## 精确关键字过滤
from django_filters.rest_framework import DjangoFilterBackend
# 自定义模糊过滤和范围过滤
from goods.filters import GoodsFilter
# 模糊查询
from rest_framework import filters
# 缓存mixin
from rest_framework_extensions.cache.mixins import CacheResponseMixin
# 限速
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

##################


# 继承generics.GenericAPIView和mixins.ListModelMixin
"""
class GoodsListView(mixins.ListModelMixin,  # list方法显示多个数据
                    # mixins.CreateModelMixin, # 如果有post请求的创建方法,添加这个继承
                    generics.GenericAPIView,
                    ):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
"""


# 继承generics.ListAPIView
class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    GenericViewSet继承 GenericAPIView 以及 ViewSetMixin
    而GenericAPIView中没有定义get post等方法,所以使用GenericViewSet的时候需要自己定义get post等等的方法  只不过这个配置是在urls重构的时候配置的
    所以我们还要继承mixins.ListModelMixin,来完成定义get的方法
    而且需要注意的是  使用 viewset 需要对urls.py重构
    APIView提供get post等方法  mixins提供 list create等行为 两者互相绑定才能实现请求对应动作  在重构urls的时候配置
    """
    # authentication_classes = (TokenAuthentication,)
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all().order_by('add_time')
    serializer_class = GoodsSerializer
    # 指明是按照那个规则分页
    pagination_class = GoodsSetPagination
    # 过滤条件,模糊查询
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    # 注意这里定义模糊搜索的字段是model中定义的字段,前端发送的变量名
    """
    这里写字段名的时候可以增加特殊符号产生特殊效果
    ^name  意味着 从name中模糊搜索必须从头匹配
    =name                         精确过滤
    @name                         全文搜索
    $name                         正则搜索
    """
    search_fields = ('name', 'goods_desc', 'goods_brief')
    ordering_fields = ('sold_num', 'shop_price',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 商品分类列表数据
class GoodsCategoryViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """
    list:
        商品分类的列表功能
    retrieve:
        获取商品分类详情
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = GoodsCategory.objects.filter(category_type=1)
    # 不需要分页 过滤 排序 模糊查询，只需要将数据序列化后输出 所以需要GoodsCategorySerializer
    serializer_class = GoodsCategorySerializer
    # 每一个 ViewSet对应一个Serializer【pagination_class，filter_backends，filter_class】
    # 相对应的 还得注册相应的router
    # 分类具有层级结构,所以这里我们只获取一级分类,然后定制一下GoodsCategorySerializer,让分类具有层级
    # 层级的实现是通过 1中有2,2中有3实现的
    # 实现完成层级,还要实现Retrieve,单独获取某个分类,这就需要继承mixins.RetrieveModelMixin,它的内部封装了
    # Retrieve行为,只要继承这个即可,router会自动配置url=.../categorys/(?P<pk>\d+?)/这种路由


class HotSearchsViewset(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    网站首页的轮播图接口
    list:
        获取首页轮播图列表
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializers


class IndexCategoryViewSet(CacheResponseMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商标商品展示
    list:
        获取首页商标商品展示的数据
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer
