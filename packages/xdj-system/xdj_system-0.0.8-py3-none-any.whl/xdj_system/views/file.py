# -*- coding: utf-8 -*-

"""
@Remark:
"""
from rest_framework import serializers

from xdj_system.models import FileModel
from xdj_utils.serializers import CustomModelSerializer
from xdj_utils.viewset import CustomModelViewSet


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        return str(instance.url)

    class Meta:
        model = FileModel
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class FileViewSet(CustomModelViewSet):
    """
    文件管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer
    filter_fields = ['name', ]
