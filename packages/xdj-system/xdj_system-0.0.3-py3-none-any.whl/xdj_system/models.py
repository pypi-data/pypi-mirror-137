import hashlib
import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from xdj_utils.models import CoreModel, table_prefix
from django.utils.translation import gettext_lazy as _

from django.conf import settings

STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
)


class User(AbstractUser,CoreModel):
    username = models.URLField( verbose_name=_('用户名'), help_text=_('用户名'), unique=True,default=uuid.uuid4)

    avatar = models.URLField( verbose_name=_('头像'), help_text=_('头像'), null=True, blank=True)
    nickname = models.CharField(verbose_name=_('昵称'), help_text=_('昵称'), max_length=100, null=True, blank=True, unique=True)

    gender = models.SmallIntegerField(default=2,verbose_name=_('性别'), help_text=_('性别'), choices=((1, '男'), (0, '女'), (2, '未知')), null=True, blank=True)
    language = models.CharField(verbose_name=_('语言'), help_text=_('语言'), max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name=_('城市'), help_text=_('城市'), max_length=200, null=True, blank=True)
    province = models.CharField(verbose_name=_('省份'), help_text=_('省份'), max_length=200, null=True, blank=True)
    country = models.CharField(verbose_name=_('国家'), help_text=_('国家'), max_length=200, null=True, blank=True)
    birthday = models.DateTimeField(verbose_name=_('出生日期'), help_text=_('出生日期'), null=True, blank=True)
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")

    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")

    role = models.ManyToManyField(to='xdj_system.Role', verbose_name='关联角色', db_constraint=False, help_text="关联角色")

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding='UTF-8')).hexdigest())

    def save(self, *args, **kwargs):
        super(User, self).save(*args,**kwargs)
        for r in settings.DEFAULT_ROLE or []:
            try:
               ro = Role.objects.get(id=r)
               self.role.add(ro)
            except Role.DoesNotExist:
                pass

    class Meta:
        db_table = table_prefix + "system_users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)



class Role(CoreModel):
    name = models.CharField(max_length=64, verbose_name="角色名称", help_text="角色名称")
    key = models.CharField(max_length=64, verbose_name="权限字符", help_text="权限字符")
    sort = models.IntegerField(default=1, verbose_name="角色顺序", help_text="角色顺序")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="角色状态", help_text="角色状态")
    ADMIN_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    admin = models.IntegerField(choices=ADMIN_CHOICES, default=0, verbose_name="是否为admin", help_text="是否为admin")
    DATASCOPE_CHOICES = (
        (0, "仅本人数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    data_range = models.IntegerField(default=0, choices=DATASCOPE_CHOICES, verbose_name="数据权限范围", help_text="数据权限范围")
    remark = models.TextField(verbose_name="备注", help_text="备注", null=True, blank=True)
    menu = models.ManyToManyField(to='xdj_system.Menu', verbose_name='关联菜单', db_constraint=False, help_text="关联菜单")
    permission = models.ManyToManyField(to='xdj_system.Permission', verbose_name='关联菜单的接口按钮', db_constraint=False,
                                        help_text="关联菜单的接口按钮")

    class Meta:
        db_table = table_prefix + 'system_role'
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
        ordering = ('sort',)

class Button(CoreModel):
    name = models.CharField(max_length=64,unique=True, verbose_name="权限名称", help_text="权限名称")
    value = models.CharField(max_length=64,unique=True, verbose_name="权限值", help_text="权限值")

    class Meta:
        db_table = table_prefix + "system_button"
        verbose_name = '权限标识表'
        verbose_name_plural = verbose_name
        ordering = ('-name',)

class Menu(CoreModel):
    parent = models.ForeignKey(to='xdj_system.Menu', on_delete=models.CASCADE, verbose_name="上级菜单", null=True, blank=True,
                               db_constraint=False, help_text="上级菜单")
    icon = models.CharField(max_length=64, verbose_name="菜单图标", null=True, blank=True, help_text="菜单图标")
    name = models.CharField(max_length=64, verbose_name="菜单名称", help_text="菜单名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    is_link = models.IntegerField(choices=ISLINK_CHOICES, default=0, verbose_name="是否外链", help_text="是否外链")
    is_catalog = models.IntegerField(choices=ISLINK_CHOICES, default=0, verbose_name="是否目录", help_text="是否目录")
    web_path = models.CharField(max_length=128, verbose_name="路由地址", null=True, blank=True, help_text="路由地址")
    component = models.CharField(max_length=128, verbose_name="组件地址", null=True, blank=True, help_text="组件地址")
    component_name = models.CharField(max_length=50, verbose_name="组件名称", null=True, blank=True, help_text="组件名称")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="菜单状态", help_text="菜单状态")
    CACHE_CHOICES = (
        (0, '禁用'),
        (1, "启用")
    )
    cache = models.IntegerField(choices=CACHE_CHOICES, default=0, verbose_name="是否页面缓存", help_text="是否页面缓存")
    visible = models.BooleanField(default=True, verbose_name="侧边栏中是否显示", help_text="侧边栏中是否显示")

    class Meta:
        db_table = table_prefix + "system_menu"
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name
        ordering = ('sort',)


class Permission(CoreModel):
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    api = models.CharField(max_length=200, verbose_name="接口地址", help_text="接口地址")
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True, help_text="接口请求方法")

    class Meta:
        db_table = table_prefix + "system_permission"
        verbose_name = '菜单权限表'
        verbose_name_plural = verbose_name
        ordering = ('-api',)


class Dictionary(CoreModel):
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name="编码", help_text="编码")
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="显示名称", help_text="显示名称")
    value = models.CharField(max_length=100, blank=True, null=True, verbose_name="实际值", help_text="实际值")
    parent = models.ForeignKey(to='self', related_name='sublist', db_constraint=False, on_delete=models.PROTECT,
                               blank=True, null=True,
                               verbose_name="父级", help_text="父级")
    STATUS_CHOICES = (
        (0, "禁用"),
        (1, "启用"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态", help_text="状态")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    remark = models.CharField(max_length=2000, blank=True, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = table_prefix + 'dictionary'
        verbose_name = "字典表"
        verbose_name_plural = verbose_name
        ordering = ('sort',)


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True, help_text="请求模块")
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True, help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True, help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True, help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True, help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True, help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = table_prefix + 'system_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


def media_img_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('media/imgs', h[0:1], h[1:2], h + ext.lower())


class ImgModel(CoreModel):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名称", help_text="名称")
    ext = models.CharField(max_length=50, null=True, blank=True, verbose_name="拓展", help_text="拓展")
    size = models.IntegerField( null=True, blank=True, verbose_name="大小", help_text="大小")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="链接", help_text="链接")
    path = models.CharField(max_length=255, null=True, blank=True, verbose_name="路径", help_text="路径")
    file = models.ImageField(upload_to=media_img_name)
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        if not self.size:
            self.size = self.file.size
        if not self.url:
            self.size = self.file.url
        if not self.path:
            self.size = self.file.path
        if not self.ext:
            name, self.ext = os.path.splitext(self.path)
        if not self.name :
            self.name, ext = os.path.splitext(self.path)
        super(ImgModel, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + 'img'
        verbose_name = '图片管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('media/files', h[0:1], h[1:2], h + ext.lower())


class FileModel(CoreModel):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="名称", help_text="名称")
    ext = models.CharField(max_length=50, null=True, blank=True, verbose_name="拓展", help_text="拓展")
    size = models.IntegerField(null=True, blank=True, verbose_name="大小", help_text="大小")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="链接", help_text="链接")
    path = models.CharField(max_length=255, null=True, blank=True, verbose_name="路径", help_text="路径")
    file = models.FileField(upload_to=media_file_name)
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        if not self.size:
            self.size = self.file.size
        if not self.url:
            self.size = self.file.url
        if not self.path:
            self.size = self.file.path
        if not self.ext:
            name, self.ext = os.path.splitext(self.path)
        if not self.name:
            self.name = self.md5sum
        super(FileModel, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + 'file'
        verbose_name = '文件管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
