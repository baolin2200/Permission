#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/1/11

from django.template import Library

from django.conf import settings
import re

register = Library()  # register的名字是固定的,不可改变


@register.inclusion_tag("rbac/menu.html")    # 使用装饰器 register.filter  即可定义一个过滤器
def menu(request):
    permission_menu_list = request.session.get(settings.PERMISSION_MENU_SESSION_KEY)
    # 获取 用户请求的 路径
    current_url = request.path_info

    per_dic = {}
    for item in permission_menu_list:
        if not item["pid"]:
            per_dic[item["id"]] = item

    for item in permission_menu_list:
        reg = settings.REX_FORMAT % (item["url"])
        if not re.match(reg, current_url):
            continue
        if item["pid"]:
            per_dic[item["pid"]]["active"] = True
        else:
            item["active"] = True

    menu_result = {}
    for item in per_dic.values():
        menu_id = item["menu_id"]
        if menu_id in menu_result:
            temp = {"id": item["id"], "title": item["title"], "url": item["url"], "active": item.get("active", False)}
            menu_result[menu_id]["children"].append(temp)

            if item.get("active", False):
                menu_result[menu_id]["active"] = item.get("active", False)
        else:
            menu_result[menu_id] = {
                "menu_name": item["menu_name"],
                "active": item.get("active", False),
                "children": [
                    {"id": item["id"], "title": item["title"], "url": item["url"], "active": item.get("active", False)}
                ]
            }
    print(menu_result)
    return {"menu_result": menu_result}
