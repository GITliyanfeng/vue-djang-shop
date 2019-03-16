# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 0012 12:41
# @Author  : __Yanfeng
# @Site    : 
# @File    : excel.py
# @Software: PyCharm
import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


# excle文件的导入
class ListImportExcelPlugin(BaseAdminPlugin):
    # 定义默认为False不加载  <在定义的adminx中可以用True将其覆盖掉,开启插件>
    import_excel = False

    # 插件入口函数,返回的是布尔值,如果是True,那么就会加载这个插件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    # 限制
    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string(template_name='xadmin/excel/model_list.top_toolbar.html',
                                             context={'context': context}))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
