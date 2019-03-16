# -*- coding: utf-8 -*-
# __author__ : py_lee
# __time__   : '18-12-16 下午3:24'

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# 接收器接收的是post_save方法,接收的模型是User
@receiver(post_save, sender=User)
# 当信号被接收的时候会判断这个信号是不是在User中新建的一个对象[新的]
def create_user_expand(sender, instance=None, created=False, **kwargs):
    """
    接收对User表信号并且处理信号
    注意当前app使用信号之后需要在apps.py脚本中重载信号脚本,将当前的脚本载入到app中
    :param sender: 模型
    :param instance: 模型的实例
    :param create: 是否是新建的
    :param kwargs: 其他参数
    :return:
    """
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
