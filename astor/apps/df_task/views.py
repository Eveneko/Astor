from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse

from apps.df_user import user_decorator
from .models import Task
from df_user.models import UserInfo, UserBuyAlgorithm
from df_goods.models import GoodsInfo, TypeInfo


import os
import uuid
import datetime


@user_decorator.login
def index(request):
    """
    算法任务管理主页
    API:
    - GET
        - ^/task/
    :param request: 请求对象
    :return: 渲染网页
    """
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    algorithm_num = len(GoodsInfo.objects.all())
    user_num = len(UserInfo.objects.all())
    task_set = Task.objects.all().filter(task_user=user).order_by("-task_start_time")
    task_set_num = len(task_set)
    if task_set_num > 5:
        task_set = task_set[:4]
    context = {
        'title': '用户中心',
        'uid': user_id,
        'user': user,
        'algorithm_num': algorithm_num,
        'user_num': user_num,
        'task_set': task_set,
        'task_set_num': task_set_num
    }
    return render(request, 'df_task/index.html', context)


@user_decorator.login
def creat_task(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])

    user_buy_algorithm = UserBuyAlgorithm.objects.filter(user_id=user_id)
    ua_set = set()
    for ua in user_buy_algorithm:
        ua_set.add(GoodsInfo.objects.get(id=ua.algorithm_id))
    algorithm_info = ua_set

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
    task_set = Task.objects.all().filter(task_user=user).order_by("-task_start_time")
    context = {
        'title': '用户中心',
        'uid': user_id,
        'user': user,
        'task_set': task_set,
        'task_set_num': len(task_set)
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
        tran_id = transaction.savepoint()  # 保存事务发生点
        try:
            user_id = request.session['user_id']
            user = UserInfo.objects.get(id=request.session['user_id'])
            File = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not File:
                return HttpResponse("No files for upload!")
            path = "static/Data/" + str(user_id)
            file_uuid = str(uuid.uuid4())
            if not os.path.exists(path):
                os.mkdir(path)
            destination = open(os.path.join(path, file_uuid), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in File.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            return HttpResponse("Upload over!")
        except Exception as e:
            print("%s" % e)
            print('未完成数据上传')
            transaction.savepoint_rollback(tran_id)  # 事务任何一个环节出错，则事务全部取消
            return HttpResponse("Upload Fail!")


def upload_task_config(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        tran_id = transaction.savepoint()  # 保存事务发生点
        user_id = request.session['user_id']
        user = UserInfo.objects.get(id=request.session['user_id'])
        context = {
            'title': '用户中心',
            'uid': user_id,
            'user': user,
        }
        try:
            algorithm = request.POST.get("algorithm")
            cpu = request.POST.get("cpu").split(' ')[0]
            mem = request.POST.get("mem").split(' ')[0]
            dataset = request.POST.get("dataset").split(',')[1]
            time = datetime.time()
            # out_uuid = run_sh.run(user_id, algorithm, dataset, cpu, mem)

            task = Task()
            task.task_user = user
            task.task_algorithm = GoodsInfo.objects.get(gtitle=algorithm)
            task.cpu = cpu
            task.memory = mem
            # task.task_start_time = time
            task.output = out_uuid
            task.task_data_url = dataset
            task.save()

            return render(request, 'df_task/task_record.html', context)
        except Exception as e:
            transaction.savepoint_rollback(tran_id)  # 事务任何一个环节出错，则事务全部取消
            return HttpResponse(e)