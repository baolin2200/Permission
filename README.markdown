rbac公共权限管理 
==
    需求的分析：
    	- 一个包含正则表达式URL是一个权限
    	- 业务需求
        - 不同权限组 看到不同的编辑管理
        - 不同权限组 看到不同的左侧菜单
    
    用户菜单显示：
        - URL中不包含正则的能成为菜单
        - 菜单默认选中（删除主机，主机列表应该被选中）    
        - 用户登录成功后，获取 权限+权限组+菜单
        - 放入session的另外一个key中 用于专门做菜单的


###使用方法：
```python
rbac 组件，目的是创建公共的 app 组件，用于所有系统增加权限管理；

1.将 rbac 组件添加到 project 中

2.将 rbac APP中的 migrations 目录除了__init__.py 文件删除

3.录入权限：5个类，7张表

4.配置文件：
    - 中间件
        - # 增加中间件配置路径
            MIDDLEWARE = [
                # ....
                'rbac.middleware.rbac.RbacMiddleware'
            ]
    - 新增配置文件
        - # rbac 权限配置##########################
            # 静态文件目录
            STATICFILES_DIRS = (
                os.path.join(BASE_DIR, 'static'),
            )
            
            # 用户登陆权限key
            PERMISSION_DICT_SESSION_KEY = "user_permission_dict_key"
            PERMISSION_MENU_SESSION_KEY = "user_permission_menu_key"
            
            # 定义 正则匹配的 硬限制 ^开头  结尾$
            REX_FORMAT = "^%s$"
            
            # 定义 访问权限 白名单
            VALID_LIST = [
                "/login/",
                "^/admin/.*"
            ]
            
5.页面自动生成菜单
    - 在项目模板中，首行引入 rbac 的inclusion_tag
{% load rbac %}       {# 导入rbac文件 #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/rbac/rbac.css">      {# 引入rbac 生成菜单样式 #}
    <style>
        .pg-header{
            height:48px;
            background-color: cornflowerblue;
        }
        body{
            margin: 0;
        }
        .pg-content .menu{
            width: 230px;
            background-color: #dddddd;
            position: absolute;
            left: 0;
            top: 48px;
            bottom:0;
        }
        .pg-content .content{
            left: 230px;
            position: absolute;
            right: 0;
            top: 48px;
            bottom:0;
            overflow: auto;
        }
    </style>
    {% block css %}
    {% endblock %}1
</head>
<body>

    <div class="pg-header">头部菜单</div>
    <div class="pg-content">
        <div class="menu">
            {# 自定义的模板数据 #}
            {% menu request %}          {# 生成动态菜单 #}

        </div>

        <div class="content">
            {% block content %}
            {% endblock %}
        </div>
    </div>
    {% block js %}
    {% endblock %}
</body>
</html>
        
```
    















###引用rbac 权限管理
####注册apps 到settings的INSTALLED_APPS 中 及 后续 settings 配置
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    "rbac"                      # 注册 app
]

# 用户登陆权限key
PERMISSION_DICT_SESSION_KEY = "user_permission_dict_key"

# 定义 正则匹配的 硬限制 ^开头  结尾$
REX_FORMAT = "^%s$"

# 定义 访问权限 白名单
VALID_LIST = [
    "/login/",
    "^/admin/.*"
]

```

####设置rbac权限管理的表结构
```python
from django.db import models

class UserInfo(models.Model):
    '''
        用户表:
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


class Permission(models.Model):
    '''
        权限表
            用户
                1   用户列表        /users/                   1
                2   添加用户        /users/add/               1
                3   删除用户        /users/del/(\d+)/         1
                4   修改用户        /users/edit/(\d+)/        1
    '''
    title = models.CharField(verbose_name="权限名称", max_length=32)
    url = models.CharField(verbose_name="含正则url", max_length=255)
    code = models.CharField(verbose_name="权限代码", max_length=32)

    # 一个权限属于多个 权限组
    group = models.ForeignKey(verbose_name="所属权限组", to="PermissionGroup")

    def __str__(self):
        return self.title
```

####用户登陆后获取用户权限信息
```python
from django.conf import settings


def init_permission(request, obj):
    '''
    用于用户登陆后的，权限信息初始化；并将信息写入到 session 中
    :param request:     请求相关的 对象信息
    :param obj:         为登陆的用户
    :return:
    '''
    # test = obj.roles.all().values("title", "permissions__title")
    # 根据用户信息obj 关联到角色表  获取该角色的 权限表 id 不为空的值； 并通过 distinct 去重；
    permission_list = obj.roles.filter(permissions__id__isnull=False).values(
        "permissions__title",
        "permissions__url",
        "permissions__code",
        "permissions__group",
    ).distinct()

    permission_dict = {}

    for permission in permission_list:
        url = permission.get("permissions__url")
        code = permission.get("permissions__code")
        group_id = permission["permissions__group"]
        if group_id in permission_dict:
            permission_dict[group_id]["urls"].append(url)
            permission_dict[group_id]["codes"].append(code)
        else:
            permission_dict[group_id] = {"urls": [url, ], "codes": [code, ]}
    '''
    # 将 用户权限信息，依照一下格式 存储到 session 中
        {
            1:
                {
                    'urls': ['/users/', '/users/add/', '/users/edit/(\\d+)/'],
                    'codes': ['list', 'add', 'edit']
                },
            2: 
                {
                    'urls': ['/hosts/', '/hosts/add/', '/hosts/edit/(\\d+)/'], 
                    'codes': ['list', 'add', 'edit']
                }
        }
    '''

    # 将数据放到 session 中：
    request.session[settings.PERMISSION_DICT_SESSION_KEY] = permission_dict
```

####通过中间件 验证用户 访问的 urls 路径是否正确
```python
from django.conf import settings
from django.shortcuts import redirect, HttpResponse, render
import re


# 该 MiddlewareMixin 类为默认继承类，在Django 1.10 之后需要该类的继承，1.7-1.8 无需该类继承
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):

        # 当前用户请求的url
        current_url = request.path_info

        # 如果 URL 存在 白名单中 /login/ ；都直接通过，不进行权限验证
        for valid in settings.VALID_LIST:
            if re.match(valid, current_url):
                return None

        # 当前用户的所有权限值
        permission_dict = request.session.get(settings.PERMISSION_DICT_SESSION_KEY)

        # print(permission_dict)

        if not permission_dict:
            return HttpResponse("用户没有登陆信息")

        # 用户权限和当前url进行匹配
        tag = False
        for item in permission_dict.values():
            urls = item["urls"]
            codes = item["codes"]
            for i in urls:

                # 定义 正则匹配的 硬限制 ^开头  结尾$ settings 中定义 格式
                i = settings.REX_FORMAT % (i,)
                if re.match(i, current_url):
                    tag = True
                    # 如果匹配成功，在 request.permission_codes 添加codes 值 'codes': ['list', 'add', 'del', 'edit']
                    # 可以在templates 中直接引用 request.permission_codes 中值 ['list', 'add', 'del', 'edit']
                    request.permission_codes = codes
                    break
            if tag:
                break

        if not tag:
            return HttpResponse("无权访问")
```






















