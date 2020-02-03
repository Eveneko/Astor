from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.db import transaction
from django.http.response import JsonResponse
from hashlib import sha1
from django.core.exceptions import ObjectDoesNotExist

from .models import UserInfo, UserBuyAlgorithm
from .forms import RegisterForm, LoginForm, UserInfoForm
from . import user_decorator


def register(request):
    """
    ^/user/register/
    注册页面请求
    :param request: 请求对象
    :return: 渲染注册页面
    """
    context = {'title': '用户注册'}
    if request.method == 'GET':
        # Get请求，初始化登录表单供用户填写
        # print('GET: user:register')
        register_form = RegisterForm()
        return render(request, 'system/register.html', locals())
    elif request.method == 'POST' and request.POST:
        # print('POST: user:register' + '\n%s' % request.POST)
        register_form = RegisterForm(data=request.POST)
        # 满足条件则将输入内容传递给form对象
        if register_form.is_valid():
            print('Form Valid')
            username = register_form.clean_username()
            password = register_form.clean_password()
            email = register_form.clean_email()
            # 密码加密
            s1 = sha1()
            s1.update(password.encode('utf8'))
            encrypted_pwd = s1.hexdigest()
            # 创建对象
            UserInfo.objects.create(uname=username, upwd=encrypted_pwd,
                                    uemail=email)
            # 注册成功
            context['title'] = '用户登陆'
            context['status'] = 'SUCCESS'
            context['username'] = username
            return render(request, 'system/login.html', context)
        else:
            context['status'] = 'FAIL'
            error_msg = eval(register_form.errors.as_json())
            if 'username' in error_msg.keys():
                context['username_error_msg'] = error_msg['username'][0]['message']
            if 'email' in error_msg.keys():
                context['email_error_msg'] = error_msg['email'][0]['message']
            if 'password' in error_msg.keys():
                context['password_error_msg'] = error_msg['password'][0]['message']
            if 'confirm_pwd' in error_msg.keys():
                context['confirm_pwd_error_msg'] = error_msg['confirm_pwd'][0]['message']
            # 返回错误信息并重新注册
            return render(request, 'system/register.html', context)
    else:
        raise Exception("Unhandled Request")


def login(request):
    """
    登录界面请求
    请求页面：GET:  ^/user/register/
    请求登录：POST: ^/user/register/csrfmiddlewaretoken={% csrf_token %}&username={% username %}&password={% password %}
    :param request: 请求对象
    :return: 渲染注册页面
    """
    context = {'title': 'USER_LOGIN', 'status': 'SUCCESS'}
    if request.method == 'GET':
        print('GET: user:login')
        uname = request.COOKIES.get('uname', '')
        login_form = LoginForm()
        return render(request, 'system/login.html', locals())
    elif request.method == 'POST' and request.POST:
        print('POST: user:login')
        login_form = LoginForm(data=request.POST)
        # 满足条件则将输入内容传递给form对象
        if login_form.is_valid():
            print('Form Valid')
            username = login_form.clean_username()
            password = login_form.clean_password()
            remember_password = login_form.clean_remember_password()
            # 验证用户
            users = UserInfo.objects.filter(uname=username)
            if len(users) > 1:
                raise Exception('出现多个同名用户')
            elif len(users) == 0:
                context['status'] = 'FAIL'
                context['username_error_msg'] = 'USER_NOT_FOUND'
            else:
                # 验证密码
                s1 = sha1()
                s1.update(password.encode('utf8'))
                if s1.hexdigest() != users[0].upwd:
                    print('PASSWORD_ERROR')
                    context['status'] = 'FAIL'
                    context['password_error_msg'] = 'PASSWORD_ERROR'
                else:
                    print('LOGIN_SUCCESS')
                    # 验证成功，添加Cookie完成跳转
                    url = request.COOKIES.get('url', '/')
                    red = HttpResponseRedirect(url)
                    if remember_password:
                        red.set_cookie('uname', username)
                    else:
                        red.set_cookie('uname', '', max_age=-1)
                    request.session['user_id'] = users[0].id
                    request.session['user_name'] = username
                    return red
            return render(request, 'system/login.html', context)
        else:
            # 表单错误
            print(login_form.errors)
            context['status'] = 'FAIL'
            error_msg = eval(login_form.errors.as_json())
            if 'username' in error_msg.keys():
                context['username_error_msg'] = error_msg['username'][0]['message']
            if 'password' in error_msg.keys():
                context['password_error_msg'] = error_msg['password'][0]['message']
            print(context)
            return render(request, 'system/login.html', context)
            # raise Exception('表单解析异常')
    else:
        raise Exception("Unhandled Request")


def logout(request):  # 用户登出
    request.session.flush()  # 清空当前用户所有session
    return redirect(reverse("df_goods:index"))


@user_decorator.login
@transaction.atomic
def info(request):  # 用户中心
    """
    用户中心界面
    # TODO: 将原子性限制加到POST请求限制内
    :param request:
    :return:
    """
    user = UserInfo.objects.get(id=request.session.get('user_id'))
    context = {
        'title': '用户中心',
        'user_name': user.uname,
        'user_email': user.uemail,
        'user_phone': user.phone
    }

    if request.method == 'GET':
        print(context)
        return render(request, 'df_user/user_center_info.html', context)
    elif request.method == 'POST' and request.POST:
        print(request.POST)
        user_info_form = UserInfoForm(data=request.POST)
        if user_info_form.is_valid():
            print('Form Valid')
            # TODO: 表单异常回显
            user.uemail = user_info_form.cleaned_data['uemail']
            user.phone = user_info_form.cleaned_data['phone']
            print(user.phone)
            user.save()
            context['user_email'] = user.uemail
            context['user_phone'] = user.phone
            return render(request, 'df_user/user_center_info.html', context)
        else:
            print(user_info_form.errors)
            context['status'] = 'FAIL'
            error_msg = eval(user_info_form.errors.as_json())
            if 'uemail' in error_msg.keys():
                context['email_error_msg'] = error_msg['uemail'][0]['message']
            if 'phone' in error_msg.keys():
                context['phone_error_msg'] = error_msg['phone'][0]['message']
            print(context)
            return render(request, 'df_user/user_center_info.html', context)
    else:
        raise Exception('UNSUPPORTED HTTP METHOD')


def revise_info_handle(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        # user.uname = request.POST.get('name')
        user.uemail = request.POST.get('uemail')
        user.phone = request.POST.get('phone')
        user.save()
    # context = {
    #     'page_name': 1,
    #     'title': '用户中心',
    #     'user': user,
    # }
    # return render_to_response('df_user/user_center_info.html',
    #                           context,
    #                           context_instance=RequestContext(request))
    return redirect(reverse('df_user:info'))


# @user_decorator.login
def my_algorithm(request):
    """
    获取用户收藏的算法
    API:
    - GET:
        - ^/user/algorithm/
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_buy_algorithm = list(UserBuyAlgorithm.objects
                                  .all()
                                  .values('algorithm__id', 'algorithm__name', 'algorithm__description',
                                          'algorithm__detail', 'algorithm__cpu_price', 'algorithm__gpu_price',
                                          'algorithm__pic_path', 'algorithm__cfg_template', 'algorithm__modify_time',
                                          'algorithm__type__name')
                                  .filter(user_id=request.session['user_id']))
        context = {'title': 'User Like Algorithm'}
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
        context['count'] = len(user_like_algorithm_list)
        context['user_like_algorithm_list'] = user_like_algorithm_list
        try:
            user_like_algorithm_list_id = UserBuyAlgorithm.objects \
                .all().values('algorithm_id').filter(
                user__id=request.session['user_id'],
            )
            tmp = []
            for a in user_like_algorithm_list_id:
                tmp.append(int(a['algorithm_id']))
            user_like_algorithm_list_id = tmp
        except ObjectDoesNotExist:
            user_like_algorithm_list_id = []
        context['user_like_algorithm_list_id'] = user_like_algorithm_list_id
        print(user_buy_algorithm)
        # return JsonResponse(context)
        return render(request, 'df_user/user_my_algorithm.html', context)
    elif request.method == 'POST' and request.POST:
        raise Exception('UNSUPPORTED HTTP METHOD')
    else:
        raise Exception('UNSUPPORTED HTTP METHOD')
