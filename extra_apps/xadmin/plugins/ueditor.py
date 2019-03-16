# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 0012 9:39
# @Author  : __Yanfeng
# @Site    : 
# @File    : ueditor.py
# @Software: PyCharm

import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, ModelAdminView, UpdateAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.conf import settings


class XadminUEditorWidget(CKEditorUploadingWidget):
    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):
    def get_field_style(self, attrs, db_field, style, **kwargs):
        # 通过判断配置中是否设置field的style以及model中定义的字段是否是UEditorField
        # 来判断是否使用ueditor来渲染当前的内容
        if style == 'ueidtor':
            if isinstance(db_field,RichTextUploadingField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget': XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="%s"></script>' % (
                    settings.STATIC_URL + "ckeditor/ckeditor-init.js")
        js += '<script type="text/javascript" src="%s"></script>' % (
                    settings.STATIC_URL + "ckeditor/ckeditor/ckeditor.js")
        nodes.append(js)


# 将配置好的插件注册到可以在修改数据以及添加数的时候使用 注意在插件目录的__init__文件中将写的插件文件的名字添加进去
xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)
