from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse

from apps.df_user import user_decorator
from df_user.models import UserInfo
from .models import Task
from df_user.models import UserInfo, UserBuyAlgorithm
from df_goods.models import GoodsInfo, TypeInfo
from django.db import transaction

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
    user_buy_algorithm = list(UserBuyAlgorithm.objects
                              .all()
                              .values('algorithm__id', 'algorithm__name')
                              .filter(user_id=request.session['user_id']))
    context = {'title': 'User Like Algorithm'}
    try:
        user_like_algorithm_list = list(
            UserBuyAlgorithm.objects
                .all()
                .values('algorithm__id', 'algorithm__name')
                .filter(user__id=request.session['user_id'], ))
    except ObjectDoesNotExist:
        user_like_algorithm_list = []
    context['user_like_algorithm_count'] = len(user_like_algorithm_list)
    context['user_like_algorithm_list'] = user_like_algorithm_list
    user_num = len(UserInfo.objects.all())
    task_set = Task.objects.all() \
        .values("algorithm__name", "status", "update_time", "config") \
        .filter(creator=user).order_by("-update_time")
    task_set_num = len(task_set)
    if task_set_num > 5:
        task_set = task_set[:4]
    context = {
        'title': '用户中心',
        'uid': user_id,
        'user': user,
        'user_num': user_num,
        'task_set': task_set,
        'task_set_num': task_set_num,
        'user_like_algorithm_count': len(user_like_algorithm_list),
        'user_like_algorithm_list': user_like_algorithm_list
    }
    print("context['user_like_algorithm_count'] =", context['user_like_algorithm_count'])
    return render(request, 'system/index.html', context)


@user_decorator.login
def creat_task(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    try:
        user_like_algorithm_list = list(
            UserBuyAlgorithm.objects
                .all()
                .values('algorithm__id', 'algorithm__name', 'algorithm__description', 'algorithm__detail',
                        'algorithm__cpu_price', 'algorithm__gpu_price', 'algorithm__pic_path',
                        'algorithm__cfg_template', 'algorithm__modify_time', 'algorithm__type__name')
                .filter(user__id=request.session['user_id'], ))
    except ObjectDoesNotExist:
        user_like_algorithm_list = []

    context = {
        'title': 'creat_task',
        'uid': user_id,
        'user': user,
        'user_like_algorithm_list': user_like_algorithm_list,
        'user_like_algorithm_count': len(user_like_algorithm_list)
    }
    return render(request, 'df_task/creat_task.html', context)


@user_decorator.login
@transaction.atomic
def upload_config(request):
    """
    用户上传配置文件，校验文件创建配置并计算单价，等待用户执行
    TODO: finish this
    API:
    - POST:
        - /task/upload_config/
    :param request:
    :return: JsonResponse
    """
    if request.method == 'GET':
        raise Exception('UNSUPPORTED HTTP METHOD')
    elif request.method == 'POST' and request.POST:
        print(request.POST)
        algorithm_id = request.POST['algorithm'].split(':')[1]
        print(algorithm_id)
        algorithm_config = request.POST['algorithm_config']
        print(algorithm_config)
        # TODO: validate config

        # create task in database, with name user_tmp
        algorithm = GoodsInfo.objects.get(id=algorithm_id)
        creator = UserInfo.objects.get(id=request.session['user_id'])
        task = Task.objects.create(creator=creator,
                                   algorithm=algorithm,
                                   status='Not Started',
                                   config=eval(algorithm_config))
        # calculate price
        algorithm_config = eval(algorithm_config)
        cpu_core_num = sum(algorithm_config['resources']['cpu_requirement'])
        gpu_core_num = sum(algorithm_config['resources']['gpu_requirement'])
        price = algorithm.cpu_price * cpu_core_num + algorithm.gpu_price + gpu_core_num
        context = {'key': ['title', 'price', 'task_id', 'username', 'phone', 'email', 'algorithm_name', 'task_time'],
                   'title': 'Create Task',
                   'price': price,
                   'task_id': task.id,
                   'username': creator.uname,
                   'phone': creator.phone,
                   'email': creator.uemail,
                   'algorithm_name': algorithm.name,
                   'task_time': task.update_time}
        return render(request, 'df_task/place_task.html', context)
        # return JsonResponse(context)
    else:
        raise Exception('UNSUPPORTED HTTP METHOD')


@user_decorator.login
def start_task(request):
    """
    用户上传配置文件，校验文件创建配置并计算单价，等待用户执行
    TODO: Using Post request to finish this
    API:
    - GET:
        - /task/start_task/?task_id={\d}
    :param request:
    :return: JsonResponse
    """
    if request.method == 'GET':
        task_id = request.GET['task_id']
        # TODO: 验证用户对任务的所有权
        # user_id = request.session['user_id']
        # TODO: 向集群发送启动任务，获取job_name并更新数据库
        return redirect(reverse('df_task:index'))
    elif request.method == 'POST' and request.POST:
        raise Exception('UNSUPPORTED HTTP METHOD')
    else:
        raise Exception('UNSUPPORTED HTTP METHOD')


@user_decorator.login
def task_record(request):
    """
    查看任务运行记录
    API:
    - GET:
        - ^/task/task_record/
        - ^/task/task_record/?force_update=True
    :param request:
    :return:
    """
    # TODO: 验证刷新时间，默认每1分钟刷新一次，或强制刷新
    # TODO: 向后端集群发送请求更新任务状态
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    task_set = Task.objects.all() \
        .values("algorithm__name", "status", "update_time", "config") \
        .filter(creator=user).order_by("-update_time")
    # print(task_set)
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


# def upload_file(request):
#     if request.method == "POST":  # 请求方法为POST时，进行处理
#         tran_id = transaction.savepoint()  # 保存事务发生点
#         try:
#             user_id = request.session['user_id']
#             user = UserInfo.objects.get(id=request.session['user_id'])
#             File = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
#             if not File:
#                 return HttpResponse("No files for upload!")
#             path = "static/Data/" + str(user_id)
#             file_uuid = str(uuid.uuid4())
#             if not os.path.exists(path):
#                 os.mkdir(path)
#             destination = open(os.path.join(path, file_uuid), 'wb+')  # 打开特定的文件进行二进制的写操作
#             for chunk in File.chunks():  # 分块写入文件
#                 destination.write(chunk)
#             destination.close()
#
#             return HttpResponse("Upload over!")
#         except Exception as e:
#             print("%s" % e)
#             print('未完成数据上传')
#             transaction.savepoint_rollback(tran_id)  # 事务任何一个环节出错，则事务全部取消
#             return HttpResponse("Upload Fail!")


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
            config = request.POST.get("algorithm_config")
            print("config:", config)
            # dataset = request.POST.get("dataset").split(',')[1]
            # time = datetime.time()
            # # out_uuid = run_sh.run(user_id, algorithm, dataset, cpu, mem)
            #
            # task = Task()
            # task.task_user = user
            # task.task_algorithm = GoodsInfo.objects.get(gtitle=algorithm)
            # task.cpu = cpu
            # task.memory = mem
            # # task.task_start_time = time
            # task.output = out_uuid
            # task.task_data_url = dataset
            # task.save()

            return render(request, 'df_task/task_record.html', context)
        except Exception as e:
            transaction.savepoint_rollback(tran_id)  # 事务任何一个环节出错，则事务全部取消
            return HttpResponse(e)
