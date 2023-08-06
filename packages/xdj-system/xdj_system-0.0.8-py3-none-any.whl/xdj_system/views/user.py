# -*- coding: utf-8 -*-

"""
@Remark: 用户管理
"""

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from xdj_utils.json_response import SuccessResponse, ErrorResponse
from xdj_utils.serializers import CustomModelSerializer
from xdj_utils.validator import CustomUniqueValidator
from xdj_utils.viewset import CustomModelViewSet

user_model = django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)

class UserSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """

    class Meta:
        model = user_model
        read_only_fields = ["id"]
        exclude = ['password']
        extra_kwargs = {
            'post': {'required': False},
        }


class UserCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """
    # username = serializers.CharField(max_length=50,validators=[CustomUniqueValidator(queryset=user_model.objects.all(), message="账号必须唯一")])
    # password = serializers.CharField(required=False, default=make_password(
    #     hashlib.md5('admin123456'.encode(encoding='UTF-8')).hexdigest()))

    def save(self, **kwargs):
        data = super().save(**kwargs)
        return data

    class Meta:
        model = user_model
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            'post': {'required': False},
        }


class UserUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """
    username = serializers.CharField(max_length=50,validators=[CustomUniqueValidator(queryset=user_model.objects.all(), message="账号必须唯一")])
    password = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(required=False, allow_blank=True,choices=((1, '男'), (0, '女'), (2, '未知')),default=2)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        return data

    class Meta:
        model = user_model
        read_only_fields = ["id"]
        fields = "__all__"
        extra_kwargs = {
            'post': {'required': False, 'read_only': True},
        }


class UserViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = user_model.objects.exclude(is_superuser=1).all()
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
    filter_fields = ['username','name','gender','is_active']
    search_fields = ['username','name','gender','role__name']



    def user_info(self, request):
        """获取当前用户信息"""
        return SuccessResponse(data=self.get_user_info(request.user), msg="获取成功")

    def update_user_info(self, request):
        """修改当前用户信息"""
        user = request.user
        user_model.objects.filter(id=user.id).update(**request.data)
        return SuccessResponse(data=self.get_user_info(user), msg="修改成功")

    def change_password(self, request, *args, **kwargs):
        """密码修改"""
        instance = user_model.objects.filter(id=kwargs.get('pk')).first()
        data = request.data
        old_pwd = data.get('oldPassword')
        new_pwd = data.get('newPassword')
        new_pwd2 = data.get('newPassword2')
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(msg="两次密码不匹配")
            elif instance.check_password(old_pwd):
                instance.password = make_password(new_pwd)
                instance.save()
                return SuccessResponse(data=None, msg="修改成功")
            else:
                return ErrorResponse(msg="旧密码不正确")
        else:
            return ErrorResponse(msg="未获取到用户")
