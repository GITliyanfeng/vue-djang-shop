# 独立使用django的models

import os
import sys

# 获取当前脚本的路径
pwd = os.path.dirname(os.path.realpath(__file__))
# 通过当前脚本的路径找到上级目录的路径
sys.path.append(pwd + '../')
# 　如果我们要单独操作model,那么必须将model创建到项目的环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoVue.settings")
import django

django.setup()
# 注意导入model必须在配置好django环境变量以及django.setup()之后,否则导入不成功

# 导入需要操作的model
from goods.models import Goods, GoodsCategory, GoodsImage

# 测试导入是否成功
# all_categories = GoodsCategory.objects.all()
# 导入数据
from db_tools.data.product_data import row_data


def main():
    for goods_detail in row_data:
        goods_instance = Goods()
        goods_instance.name = goods_detail['name']
        goods_instance.market_price = float(goods_detail['market_price'].replace("￥", "").replace('元', ''))
        goods_instance.shop_price = float(goods_detail['sale_price'].replace("￥", "").replace('元', ''))
        goods_instance.goods_brief = goods_detail['desc'] if goods_detail['desc'] is not None else ""
        goods_instance.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
        goods_instance.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

        # 由于是外键,需要获取category外键对象
        category_name = goods_detail["categorys"][-1]
        category = GoodsCategory.objects.filter(name=category_name)

        if category:
            goods_instance.category = category[0]
        goods_instance.save()

        # 还有轮播图
        for goods_images in goods_detail['images']:
            # 生成GoodImage对象
            goods_image_instance = GoodsImage()
            # 循环遍历生成对象,为goodsimage对象添加数据
            goods_image_instance.image = goods_images
            # 在一个循环中,图片所对应的商品外键是当前商品的实例
            goods_image_instance.goods = goods_instance
            goods_image_instance.save()
    print('Done')


if __name__ == '__main__':
    main()
