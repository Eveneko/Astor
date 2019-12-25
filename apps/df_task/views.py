from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse

from hashlib import sha1
from apps.df_user import user_decorator
from django import forms

from df_user.models import GoodsBrowser, UserInfo,UserBuyAlgorithm
from df_order.models import OrderDetailInfo, OrderInfo
from df_goods.models import GoodsInfo, TypeInfo

import os


@user_decorator.login
def index(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    algorithm_num = len(GoodsInfo.objects.all())
    user_num = len(UserInfo.objects.all())
    context = {
        'title': '用户中心',
        'uid': user_id,
        'algorithm_num': algorithm_num,
        'user_num': user_num
    }
    return render(request, 'df_task/index.html', context)


def logout(request):
    request.session.flush()  # 清空当前用户所有session
    return redirect(reverse("df_goods:index"))


@user_decorator.login
def creat_task(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    user_buy_algorithm = UserBuyAlgorithm.objects.filter(user_id=user_id)
    ua_set = set()
    for ua in user_buy_algorithm:
        ua_set.add(GoodsInfo.objects.get(id=ua.algorithm_id))
    algorithm_info = ua_set
    # algorithm_info = GoodsInfo.objects.all()
    context = {
        'title': 'creat_task',
        'uid': user_id,
        'user': user,
        'algorithm_info': algorithm_info,
    }
    print(algorithm_info)
    return render(request, 'df_task/creat_task.html', context)


@user_decorator.login
def task_record(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    context = {
        'title': '用户中心',
        'uid': user_id,
        'user': user,
    }
    return render(request, 'df_task/task_record.html', context)


@user_decorator.login
def upload_data(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    context = {
        'title': '用户中心',
        'uid': user_id,
        'user': user,
    }
    return render(request, 'df_task/upload_data.html', context)


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        File = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not File:
            return HttpResponse("No files for upload!")
        destination = open(os.path.join("../../Data/", File.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in File.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("Upload over!")
