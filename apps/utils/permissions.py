# -*- coding: utf-8 -*-
# __author__ : py_lee
# __time__   : '18-12-14 下午5:02'
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    # 重载判断权限的方法,当判断请求是安全的[只读取get,options,head]返回权限为True
    # 否则判断当前操作对象的所有者是否是user
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user
