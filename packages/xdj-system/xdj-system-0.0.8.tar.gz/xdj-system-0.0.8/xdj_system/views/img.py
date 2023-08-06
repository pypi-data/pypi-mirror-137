# -*- coding: utf-8 -*-

"""
@Remark:
"""

from xdj_utils.serializers import CustomModelSerializer
from xdj_utils.viewset import CustomModelViewSet

from xdj_system.models import ImgModel


class ImgSerializer(CustomModelSerializer):


    class Meta:
        model = ImgModel
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class ImgViewSet(CustomModelViewSet):
    """
    图片管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = ImgModel.objects.all()
    serializer_class = ImgSerializer
    filter_fields = ['name', ]
