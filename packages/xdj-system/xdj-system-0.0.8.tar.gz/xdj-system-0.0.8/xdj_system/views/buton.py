# -*- coding: utf-8 -*-

"""
@author: xuan
@contact: QQ:595127207
@Created on: 2021/6/3 003 0:30
@Remark: 按钮权限管理
"""
from xdj_system.models import Button
from xdj_utils.serializers import CustomModelSerializer
from xdj_utils.viewset import CustomModelViewSet


class ButtonSerializer(CustomModelSerializer):
    """
    按钮权限-序列化器
    """

    class Meta:
        model = Button
        fields = "__all__"
        read_only_fields = ["id"]


class ButtonViewSet(CustomModelViewSet):
    """
    按钮权限接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Button.objects.all()
    serializer_class = ButtonSerializer
    permission_classes = []
