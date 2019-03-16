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
from goods.models import GoodsCategory

# 测试导入是否成功
# all_categories = GoodsCategory.objects.all()
# 导入数据
from db_tools.data.category_data import row_data


def main():
    # 遍历数据,生成对象
    for lev_1_cat in row_data:
        # 实例化一个GoodsCategory对象
        lev_1_instance = GoodsCategory()
        lev_1_instance.code = lev_1_cat['code']
        lev_1_instance.name = lev_1_cat['name']
        lev_1_instance.category_type = 1
        lev_1_instance.save()

        for lev_2_cat in lev_1_cat['sub_categorys']:
            lev_2_instance = GoodsCategory()
            lev_2_instance.code = lev_2_cat['code']
            lev_2_instance.name = lev_2_cat['name']
            lev_2_instance.category_type = 2
            lev_2_instance.parent_category = lev_1_instance
            lev_2_instance.save()

            for lev_3_cat in lev_2_cat['sub_categorys']:
                lev_3_instance = GoodsCategory()
                lev_3_instance.code = lev_3_cat['code']
                lev_3_instance.name = lev_3_cat['name']
                lev_3_instance.category_type = 3
                lev_3_instance.parent_category = lev_2_instance
                lev_3_instance.save()
    print('Done')


if __name__ == '__main__':
    main()
