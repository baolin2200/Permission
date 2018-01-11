#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/1/9
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
        "permissions__id",          # 权限ID
        "permissions__title",       # 权限名称
        "permissions__url",         # 权限url
        "permissions__code",        # 权限 code  ["list","edit","add","del"]
        "permissions__group",       # 权限组
        "permissions__group_menu_id",    # 组内菜单ID(null 表示自己为菜单，1 表示 ID为1的是它的菜单)
        "permissions__group__menu__id",     # 一级菜单ID
        "permissions__group__menu__name",   # 一级菜单名称
    ).distinct()

    # 获取权限信息 + 组 + 菜单，放入session,用于在页面自动生成动态菜单
    permission_memu_list = []
    for item in permission_list:
        val = {
            "id": item["permissions__id"],
            "title": item["permissions__title"],
            "url": item["permissions__url"],
            "pid": item["permissions__group_menu_id"],
            "menu_id": item["permissions__group__menu__id"],
            "menu_name": item["permissions__group__menu__name"],
        }
        permission_memu_list.append(val)
    request.session[settings.PERMISSION_MENU_SESSION_KEY] = permission_memu_list

    # 获取权限信息，放入session, 用于以后再中间件中权限进行匹配
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

