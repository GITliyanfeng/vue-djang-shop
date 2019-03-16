# -*- coding: utf-8 -*-
# __author__ : py_lee
# __time__   : '18-12-16 下午3:24'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from user_operation.models import UserFav

model = UserFav


# 接收器接收的是post_save方法,接收的模型是User
@receiver(post_save, sender=model)
# 当信号被接收的时候会判断这个信号是不是在User中新建的一个对象[新的]
def create_userfav(sender, instance=None, created=False, **kwargs):
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
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=model)
# 当信号被接收的时候会判断这个信号是不是在User中新建的一个对象[新的]
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    if goods.fav_num < 0:
        goods.fav_num = 0
    goods.save()
