# -*- coding: utf-8 -*-

"""
@Remark: 菜单按钮管理
"""
from xdj_system.models import Permission
from xdj_utils.serializers import CustomModelSerializer
from xdj_utils.viewset import CustomModelViewSet


class PermissionSerializer(CustomModelSerializer):
    """
    菜单按钮-序列化器
    """

    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ["id"]


class PermissionViewSet(CustomModelViewSet):
    """
    菜单按钮接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = []
