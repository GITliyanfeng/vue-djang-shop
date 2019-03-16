from django.db.models import Q

import django_filters

from goods.models import Goods


# 需要去view视图的viewset中定义filter_class = 这个类  而且 filter_backends 还是使用 DjangoFilterBackend
class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
        自定义商品过滤规则类
    """
    # 对于数字类型的过滤规则 参数 field_name:所操作的字段名  lookup_expr : 查询方式 gte 大于等于
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text='最低价格')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte', help_text='最高价格')
    # contains 是模糊查询 i开头是忽略大小写  如果不指定lookup_expr参数,那么就必须完全匹配
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    # 过滤出所选分类下的所有商品
    # method参数可以通过传递自定义函数的指针来实现自定义逻辑上的过滤
    top_category = django_filters.NumberFilter(method='top_category_filter')

    # queryset  name  value这三个参数是固定传入的参数,所以需要固定写法的写上去
    def top_category_filter(self, queryset, name, value):
        # 商品所属分类的id或者父级分类的id,商品父级分类的夫极分类的id为传递过来的value
        queryset = queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemax', 'pricemin', 'name', 'is_hot', 'is_new']
