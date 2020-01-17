from django.shortcuts import render
from apps.df_user import user_decorator
from df_user.models import UserInfo
from df_goods.models import GoodsInfo
from df_task.models import Task
# Create your views here.
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
    user = UserInfo.objects.get(id=user_id)
    algorithm_num = len(GoodsInfo.objects.all())
    user_num = len(UserInfo.objects.all())
    task_set = Task.objects.all().filter(creator=user).order_by("-creator_id")
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
    return render(request, 'system/index.html', context)