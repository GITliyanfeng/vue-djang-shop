from rest_framework import serializers
from goods.models import Goods, GoodsCategory, GoodsImage, HotSearchWords, Banner, GoodsCategoryBrand, IndexAd
from django.db.models import Q

"""
# 使用serializers.Serializer通过自定义字段来自定义 串行器
class GoodsSerializer_1(serializers.Serializer):
    # 映射Goods下的字段 类似 django form的功能
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0, )
    goods_front_image = serializers.ImageField()
    add_time = serializers.DateTimeField()

    # 创建对象的接口--对应的是GoodListView中的post方法
    def create(self, validated_data):
        # 此处的validated_data是将上面定义的字段映射从Serializer中获取数据后,打包成字典
        return Goods.objects.create(**validated_data)
        # 创建一个新的good
"""


class GoodsCategorySerializer_3(serializers.ModelSerializer):
    """
    商品分类序列化_3级别
    """

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer_2(serializers.ModelSerializer):
    """
    商品分类序列化_2级别
    """
    # GoodsCategorySerializer_2-->GoodsCategorySerializer_3
    sub_cat = GoodsCategorySerializer_3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品分类序列化
    """
    # models中的字段定义了related_name,通过这个参数就能从主表查询附表,主表中的对象找到对应字表中的对象们 1及分类找2级分类
    # 通过层级嵌套来实现分级     related_name 这个参数要和当前这里的参数保持一致
    # 在GoodsCategorySerializer-->GoodsCategorySerializer_2
    sub_cat = GoodsCategorySerializer_2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


# 既然Serializer和form是对应的,那么一定有一个ModelSerializer,来简化操作

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品序列化
    """
    # 简化操作后,直接指明映射的模型是哪一个,就可以自动形成映射关系
    category = GoodsCategorySerializer()  # 在这里实例化category对象来赋值给category,来替换仅仅能序列化为id的外键category
    # 外键映射
    images = GoodsImageSerializer(many=True)

    # ,通过fields参数来控制哪些字段被映射
    class Meta:
        model = Goods
        # 所有字段都被序列化了出来,但是外键关联都序列化为相应的id,可以通过Serializer的嵌套实现将外键id找到对应的对象
        '''
        fields = (
        "category", "name", "goods_sn", "click_num", "sold_num", "fav_num", "goods_num", "market_price", "shop_price",
        "goods_brief", "goods_desc", "ship_free", "is_new", "is_hot", "goods_front_image", "add_time",)
        '''
        # 如果本身就是返回所有的值,可以使用__all__参数
        fields = "__all__"


class UserFavGoodsSerializers(serializers.ModelSerializer):
    images = GoodsImageSerializer(many=True)
    category = GoodsCategorySerializer()

    class Meta:
        model = Goods
        fields = ('images', 'category', 'name', 'id', 'shop_price')


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandsSerializers(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


# 首页各个商品的展示
class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandsSerializers(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = GoodsCategorySerializer_2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            # 注意这个.data返回的是序列化的json数据,如果忘记这个data,那么"Object of type 'GoodsSerializer' is not JSON serializable"错误
            goods_json = GoodsSerializer(goods_ins, many=False, context={'request': self.context['request']}).data

        return goods_json

    def get_goods(self, obj):
        # 某个分类下的所有商品(包扩此分类的子分类下的商品)
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category=obj.id))
        # 使用GoodsSerializer对当前过滤出来的商品,进行序列化,就相当于传入了个queryset
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
