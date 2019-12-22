from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from hashlib import sha1
from apps.df_user import user_decorator


@user_decorator.login
def index(request):
    user_id = request.session['user_id']
    context = {
        'title': '用户中心',
        'uid': user_id,
    }
    return render(request, 'df_task/index.html', context)


def logout(request):
    request.session.flush()  # 清空当前用户所有session
    return redirect(reverse("df_goods:index"))


@user_decorator.login
def creat_task(request):
    user_id = request.session['user_id']
    context = {
        'title': '用户中心',
        'uid': user_id,
    }
    return render(request, 'df_task/creat_task.html', context)


@user_decorator.login
def task_record(request):
    user_id = request.session['user_id']
    context = {
        'title': '用户中心',
        'uid': user_id,
    }
    return render(request, 'df_task/task_record.html', context)
