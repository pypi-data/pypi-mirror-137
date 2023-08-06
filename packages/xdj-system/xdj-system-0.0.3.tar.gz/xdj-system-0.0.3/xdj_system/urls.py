# -*- coding: utf-8 -*-

"""
@Remark: 系统管理的路由文件
"""
from django.urls import path, re_path
from rest_framework import routers

from xdj_system.views.buton import ButtonViewSet
from xdj_system.views.dictionary import DictionaryViewSet
from xdj_system.views.file import FileViewSet
from xdj_system.views.img import ImgViewSet
from xdj_system.views.menu import MenuViewSet
from xdj_system.views.permission import PermissionViewSet
from xdj_system.views.operation_log import OperationLogViewSet
from xdj_system.views.role import RoleViewSet
from xdj_system.views.user import UserViewSet

system_url = routers.SimpleRouter()
system_url.register(r'button', ButtonViewSet)
system_url.register(r'menu', MenuViewSet)
system_url.register(r'permission', PermissionViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'operation_log', OperationLogViewSet)
system_url.register(r'dictionary', DictionaryViewSet)
system_url.register(r'img', ImgViewSet)
system_url.register(r'file', FileViewSet)

urlpatterns = [
    re_path('role/role_id_to_menu/(?P<pk>.*?)/', RoleViewSet.as_view({'get': 'roleId_to_menu'})),
    path('menu/web_router/', MenuViewSet.as_view({'get': 'web_router'})),
    path('user/user_info/', UserViewSet.as_view({'get': 'user_info', 'put': 'update_user_info'})),
    re_path('user/change_password/(?P<pk>.*?)/', UserViewSet.as_view({'put': 'change_password'})),

]
urlpatterns += system_url.urls
