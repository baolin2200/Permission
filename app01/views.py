from django.shortcuts import render,HttpResponse
from django.views.decorators.cache import cache_page

# 导入rbac 模块获取用户 登陆权限
from rbac.service.init_permission import init_permission

from rbac import models as models
from django.conf import settings
import re


# rbac 部分
def login(requset):
    if requset.method == "GET":
        return render(requset, "login.html")

    else:
        user = requset.POST.get("user")
        pwd = requset.POST.get("pwd")
        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if obj:
            # print("登录成功", obj)
            init_permission(requset, obj)

            return HttpResponse("登陆成功")
        else:
            return render(requset, "login.html")


def users(request):

    user_list = models.UserInfo.objects.all()

    return render(request, "users.html", {"user_list": user_list})


def users_add(request):
    return HttpResponse("useradd")


def hosts(request):

    return render(request, "hosts.html",)