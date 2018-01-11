from django.db import models

# Create your models here.


class UserInfo(models.Model):
    '''
        用户表:
        1   zhangsan    123
        2   lisi        123
        3   baolin      123

    '''
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64,)

    # 通过 用户 获取用户的 角色
    roles = models.ManyToManyField(verbose_name="用户拥有的角色", to="Role",)


class Role(models.Model):
    '''
        角色表
        1   部门经理
        2   部门主管
        3   员工
    '''
    title = models.CharField(verbose_name="角色名称", max_length=32,)

    # 用户获取角色后，通过permissions 可以获取 他的权限
    permissions = models.ManyToManyField(verbose_name="角色拥有的权限", to="Permission",)

    def __str__(self):
        return self.title


class PermissionGroup(models.Model):
    '''
        权限组 表
        1   用户权限组
        2   主机权限组
    '''
    caption = models.CharField(verbose_name="权限组名", max_length=32)
    menu = models.ForeignKey(verbose_name="所属菜单", to="Menu",)


class Menu(models.Model):
    '''
        菜单表
    '''
    name = models.CharField(max_length=32)


class Permission(models.Model):
    '''
        权限表
            用户
                1   用户列表        /users/                   1
                2   添加用户        /users/add/               1
                3   删除用户        /users/del/(\d+)/         1
                4   修改用户        /users/edit/(\d+)/        1
            主机
                1   主机列表        /hosts/                   2
                2   添加主机        /hosts/add/               2
                3   删除主机        /hosts/del/(\d+)/         2
                4   修改主机        /hosts/edit/(\d+)/        2
    '''
    title = models.CharField(verbose_name="权限名称", max_length=32)
    url = models.CharField(verbose_name="含正则url", max_length=255)
    code = models.CharField(verbose_name="权限代码", max_length=32)

    # 一个权限属于多个 权限组
    group = models.ForeignKey(verbose_name="所属权限组", to="PermissionGroup")

    # 用于判断该权限是否为 菜单   null=True  表示该字段可以为空, blank=True 表示该字段在 DjangoAdmin 中可以为空
    group_menu = models.ForeignKey(verbose_name="组内菜单", to="Permission", null=True, blank=True,)

    def __str__(self):
        return self.title
