#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/1/9

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





