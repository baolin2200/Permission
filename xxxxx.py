# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
# # Date: 2018/1/9
#
#
#
# a = [
#     {'permissions__title': '用户列表', 'permissions__url': '/users/', 'permissions__code': 'list', 'permissions__group': 1},
#     {'permissions__title': '添加用户', 'permissions__url': '/users/add/', 'permissions__code': 'add', 'permissions__group': 1},
#     {'permissions__title': '删除用户', 'permissions__url': '/users/del/(\\d+)/', 'permissions__code': 'del', 'permissions__group': 1},
#     {'permissions__title': '修改用户', 'permissions__url': '/users/edit/(\\d+)/', 'permissions__code': 'edit', 'permissions__group': 1},
#     {'permissions__title': '主机列表', 'permissions__url': '/hosts/', 'permissions__code': 'list', 'permissions__group': 2},
#     {'permissions__title': '添加主机', 'permissions__url': '/hosts/add/', 'permissions__code': 'add', 'permissions__group': 2},
#     {'permissions__title': '删除主机', 'permissions__url': '/hosts/del/(\\d+)/', 'permissions__code': 'del', 'permissions__group': 2},
#     {'permissions__title': '修改主机', 'permissions__url': '/hosts/edit/(\\d+)/', 'permissions__code': 'edit', 'permissions__group': 2},
#      ]
#
# permission_dict = {}
#
#
# # for permission in a:
# #     url = permission.get("permissions__url")
# #     code = permission.get("permissions__code")
# #     group = permission.get("permissions__group")
# #     if group in permission_dict:
# #         permission_dict[group]["urls"].append(url)
# #         permission_dict[group]["codes"].append(code)
# #         print(permission_dict[group])
# #     else:
# #         permission_dict[group] = {"urls": [url, ], "codes": [code, ]}
#
#
# for permission in a:
#     url = permission["permissions__url"]
#     code = permission["permissions__code"]
#     group = permission["permissions__group"]
#     if group in permission_dict:
#         permission_dict[group]["urls"].append(url)
#         permission_dict[group]["codes"].append(code)
#     else:
#         permission_dict[group] = {"urls": [url, ], "codes": [code, ]}
#
#
# print(permission_dict)
#
# # {'permissions__title': '用户列表', 'permissions__url': '/users/', 'permissions__code': 'list', 'permissions__group': 1},
#
#
# '''
# {
#     1: {
#         urls: [/users/,/users/add/ ,/users/del/(\d+)/],
#         codes: [list,add,del]
#     },
#     2: {
#         urls: [/hosts/,/hosts/add/ ,/hosts/del/(\d+)/],
#         codes: [list,add,del]
#     }
# }
# '''
#
# v = {
#     1:
#         {
#             'urls': ['/users/', '/users/add/', '/users/edit/(\\d+)/'],
#             'codes': ['list', 'add', 'edit']
#         },
#     2:
#         {
#             'urls': ['/hosts/', '/hosts/add/', '/hosts/edit/(\\d+)/'],
#             'codes': ['list', 'add', 'edit']
#         }
# }

import re

# v1 为规则
# current_url 为值

v1 = "^/hosts/$"

current_url = "/hosts/add/"

print(re.match(v1, current_url))


zzz = [
    {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 2, 'title': '添加用户', 'url': '/users/add/', 'pid': 1, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 3, 'title': '删除用户', 'url': '/users/del/(\\d+)/', 'pid': 1, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 4, 'title': '修改用户', 'url': '/users/edit/(\\d+)/', 'pid': 1, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 6, 'title': '添加主机', 'url': '/hosts/add/', 'pid': 5, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 7, 'title': '删除主机', 'url': '/hosts/del/(\\d+)/', 'pid': 5, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 8, 'title': '修改主机', 'url': '/hosts/edit/(\\d+)/', 'pid': 5, 'menu_id': 1, 'menu_name': '菜单一'}
]


current_url = "/hosts/del/1"

per_dic = {}

for item in zzz:
    if not item["pid"]:
        per_dic[item["id"]] = item

# print(per_dic)

for item in zzz:
    if not re.match(item["url"], current_url):
        continue
    if item["pid"]:
        per_dic[item["pid"]]["avtice"] = True
    else:
        item["avtive"] = True

print(per_dic)

result = {}

for item in per_dic.values():
    menu_id = item["menu_id"]
    if menu_id in result:
        temp = {"id": item["id"], "title":item["title"], "url": item["url"], "avtice": item.get("avtice", False)}
    else:
        result[menu_id] = {
            "menu_name": item["menu_name"],
            "avtice": item.get("avtice", False),
            "children": [
                {"id":item["id"], "title":item["title"], "url": item["url"], "avtice": item.get("avtice", False)}
            ],
        }


pppp = {
    1: {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu_name': '菜单一', 'avtive': True},
    5: {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu_name': '菜单一'}
}


eeeee = {
    1: {
        'menu_name': '菜单一',
        'active': False,
        'children': [
            {'id': 1, 'title': '用户列表', 'url': '/users/', 'avtice': False},
            {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'avtice': False}
        ]
    }
}




fff =  [
    {'id': 1, 'title': '用户列表', 'url': '/users/', 'pid': None, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 2, 'title': '添加用户', 'url': '/users/add/', 'pid': 1, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 3, 'title': '删除用户', 'url': '/users/del/(\\d+)/', 'pid': 1, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 4, 'title': '修改用户', 'url': '/users/edit/(\\d+)/', 'pid': 1, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 5, 'title': '主机列表', 'url': '/hosts/', 'pid': None, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 6, 'title': '添加主机', 'url': '/hosts/add/', 'pid': 5, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 7, 'title': '删除主机', 'url': '/hosts/del/(\\d+)/', 'pid': 5, 'menu_id': 1, 'menu_name': '菜单一'},
    {'id': 8, 'title': '修改主机', 'url': '/hosts/edit/(\\d+)/', 'pid': 5, 'menu_id': 1, 'menu_name': '菜单一'}
]



dd = {
    1: {'menu_name': '菜单一', 'active': True, 'children': [{'id': 1, 'title': '用户列表', 'url': '/users/', 'active': True}]},
    2: {'menu_name': '菜单二', 'active': False, 'children': [{'id': 5, 'title': '主机列表', 'url': '/hosts/', 'active': False}]}}

