from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator

from hashlib import sha1

from .models import UserInfo
from .forms import RegisterForm, LoginForm
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
def info(request):  # 用户中心
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by(
        "-browser_time")
    goods_list = []
    if browser_goods:
        goods_list = [browser_good.good for browser_good in
                      browser_goods]  # 从浏览商品记录中取出浏览商品
        explain = '最近浏览'
    else:
        explain = '无最近浏览'

    context = {
        'title': '用户中心',
        'page_name': 1,
        'user_phone': user.uphone,
        'user_address': user.uaddress,
        'user_name': username,
        'goods_list': goods_list,
        'explain': explain,
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request, index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by(
        '-odate')
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    context = {
        'paginator': paginator,
        'page': page,
        # 'orders_list':orders_list,
        'title': "用户中心",
        'page_name': 1,
    }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        # user.ushou = request.POST.get('ushou')
        # user.uaddress = request.POST.get('uaddress')
        # user.uyoubian = request.POST.get('uyoubian')
        # user.uphone = request.POST.get('uphone')
        user.save()
    context = {
        'page_name': 1,
        'title': '用户中心',
        'user': user,
    }
    return render(request, 'df_user/user_center_site.html', context)


@user_decorator.login
def publish(request):
    user_id = request.session['user_id']
    context = {
        'title': '用户中心',
        'uid': user_id,
    }
    return render(request, 'df_user/user_center_seller.html', context)


@user_decorator.login
def publish_handle(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 解析请求
    isDelete = request.POST.get('isDelete')
    if isDelete is None:
        isDelete = False
    gname = request.POST.get('gname')
    gpic = request.POST.get('gpic')
    gjianjie = request.POST.get('gjianjie')
    gcontent = request.POST.get('gcontent')
    gtype = request.POST.get('gtype')
    typeinfo = TypeInfo.objects.get(ttitle=gtype)
    gcode = request.POST.get('gcode')
    gdoc = request.POST.get('gdoc')

    # 创建新商品并与当前卖家关联
    good = GoodsInfo.objects.create(isDelete=isDelete, gtitle=gname, gpic=gpic,
                                    gjianjie=gjianjie, gcontent=gcontent,
                                    gtype=typeinfo, gcode=gcode, gdoc=gdoc,
                                    guser=user)

    print('user id =', user.id)
    print('good id =', good.id)
    # good = GoodsInfo.objects.get()
    return render(request, 'df_user/user_center_seller.html', None)
    # return render(request, 'df_user/user_center_seller.html', context)


@user_decorator.login
def published(request, index):
    user_id = request.session['user_id']
    print('user id =', user_id)
    goods_list = GoodsInfo.objects.filter(guser=int(user_id)).order_by(
        '-gmdf_time')
    print(goods_list)
    paginator = Paginator(goods_list, 2)
    page = paginator.page(int(index))
    context = {
        'paginator': paginator,
        'page': page,
        # 'orders_list':orders_list,
        'title': "用户中心",
        'page_name': 1,
    }
    print('page =', page)
    for goodinfo in page:
        print(goodinfo.id)
    return render(request, 'df_user/user_center_published.html', context)
