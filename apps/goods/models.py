from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class GoodsCategory(models.Model):
    """
    商品分类
        分类有三个等级
        通过一个表来定义分类的从属关系,而不是定义三个model将三个等级写死
    """
    CATEGORY_TYPES = (
        (1, '一级分类'),
        (2, '二级分类'),
        (3, '三级分类'),
    )
    name = models.CharField(max_length=30, default='', verbose_name='类别名', help_text='类别名')
    code = models.CharField(max_length=30, default='', verbose_name='类别code', help_text='类别code')
    desc = models.TextField(max_length=200, default='', verbose_name='类别描述', help_text='类别描述')
    category_type = models.IntegerField(choices=CATEGORY_TYPES, verbose_name='分类等级', help_text='分类等级')
    # parent_category自己指向自己 这里要用到self
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='父类别', related_name='sub_cat')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航', help_text='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    '''
    品牌
    '''
    category = models.ForeignKey(GoodsCategory, verbose_name='商品分类', null=True, blank=True, related_name='brands')
    name = models.CharField(max_length=30, default='', verbose_name='品牌名', help_text='品牌名')
    desc = models.TextField(max_length=200, default='', verbose_name='品牌描述', help_text='品牌描述')
    image = models.ImageField(max_length=200, upload_to='brands/',blank=True,null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '宣传品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    '''
        定义商品模型
    '''
    category = models.ForeignKey(GoodsCategory, verbose_name='商品分类', )
    name = models.CharField(max_length=200, default='', verbose_name='商品名')
    goods_sn = models.CharField(max_length=50, default='', verbose_name='商品唯一标识', )
    click_num = models.IntegerField(default=0, verbose_name='商品点击量')
    sold_num = models.IntegerField(default=0, verbose_name='商品销售量')
    fav_num = models.IntegerField(default=0, verbose_name='商品收藏量')
    goods_num = models.IntegerField(default=0, verbose_name='商品库藏量')
    market_price = models.FloatField(default=0, verbose_name='市场价格')
    shop_price = models.FloatField(default=0, verbose_name='销售价格')
    goods_brief = models.TextField(max_length=500, verbose_name='商品简述')
    # goods_desc = UEditorField(max_length=500, verbose_name=u'商品详述', imagePath='goods/images/', filePath='goods/files/',width=800, height=300,default='')
    goods_desc = RichTextUploadingField()
    ship_free = models.BooleanField(default=True, verbose_name='是否承担运费')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    is_hot = models.BooleanField(default=False, verbose_name='是否热销', help_text='是否热销')
    goods_front_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='商品主图')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    '''
        详情页轮播图管理
    '''
    goods = models.ForeignKey(Goods, verbose_name='商品', related_name='images')
    image = models.ImageField(upload_to='', verbose_name='图片', null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', )

    class Meta:
        verbose_name = '详情页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    首页轮播的商品
    """
    goods = models.ForeignKey(Goods, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='轮播图', blank=True, null=True)
    index = models.IntegerField(default=0, verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '首页轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    热搜词
    """
    keywords = models.CharField(default="", max_length=20, verbose_name="热搜词")
    index = models.IntegerField(default=0, verbose_name="排序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords


class IndexAd(models.Model):
    category = models.ForeignKey(GoodsCategory, verbose_name='商品分类', related_name='category')
    goods = models.ForeignKey(Goods, verbose_name='商品', related_name='goods')

    class Meta:
        verbose_name = '首页商品广告位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
