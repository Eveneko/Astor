from apps.df_user import user_decorator
from django.shortcuts import redirect, reverse
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
    return redirect(reverse('df_task:index'))
