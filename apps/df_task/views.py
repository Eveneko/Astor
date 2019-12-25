from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from hashlib import sha1
from apps.df_user import user_decorator
from django import forms

from df_user.models import GoodsBrowser, UserInfo
from df_order.models import OrderDetailInfo, OrderInfo
from df_goods.models import GoodsInfo, TypeInfo


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
    algorithm_info = forms.ModelChoiceField(queryset=GoodsInfo.objects.all(),
                                            required=True,
                                            empty_label="Choose Algorithm",
                                            initial="a+b")
    context = {
        'title': 'creat_task',
        'uid': user_id,
        'user': user,
        'algorithm_info': algorithm_info,
    }
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
