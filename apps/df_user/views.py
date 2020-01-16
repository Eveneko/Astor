from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse

from hashlib import sha1

from .models import GoodsBrowser, UserInfo
from . import user_decorator
from df_order.models import OrderDetailInfo, OrderInfo
from df_goods.models import GoodsInfo, TypeInfo


def register(request):
    context = {
        'title': '用户注册',
    }
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    confirm_pwd = request.POST.get('cpwd')
    email = request.POST.get('email')

    print(username, password, confirm_pwd, email)

    # 判断两次密码一致性
    if password != confirm_pwd:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(password.encode('utf8'))
    encrypted_pwd = s1.hexdigest()

    # 创建对象
    UserInfo.objects.create(uname=username, upwd=encrypted_pwd, uemail=email)
    # 注册成功
    context = {
        'title': '用户登陆',
        'username': username,
    }
    return render(request, 'df_user/login.html', context)


def register_exist(request):
    username = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=username).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登陆',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }
    return render(request, 'df_user/login.html', context)


def login_handle(request):  # 没有利用ajax提交表单
    # 接受请求信息
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    jizhu = request.POST.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)
    print(uname, upwd)
    if len(users) == 1:  # 判断用户密码并跳转
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)  # 继承与HttpResponse 在跳转的同时 设置一个cookie值
            # 是否勾选记住用户名，设置cookie
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)  # 设置过期cookie时间，立刻过期
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {
                'title': '用户名登陆',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
            }
            return render(request, 'df_user/login.html', context)
    else:
        context = {
            'title': '用户名登陆',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(request, 'df_user/login.html', context)


def logout(request):  # 用户登出
    request.session.flush()  # 清空当前用户所有session
    return redirect(reverse("df_goods:index"))


@user_decorator.login
def info(request):  # 用户中心
    username = request.session.get('user_name')
    user = UserInfo.objects.filter(uname=username).first()
    browser_goods = GoodsBrowser.objects.filter(user=user).order_by("-browser_time")
    goods_list = []
    if browser_goods:
        goods_list = [browser_good.good for browser_good in browser_goods]  # 从浏览商品记录中取出浏览商品
        explain = '最近浏览'
    else:
        explain = '无最近浏览'

    context = {
        'title': '用户中心',
        'page_name': 1,
        'user_phone': user.uphone,
        'user_address': user.uaddress,
        'user_email': user.uemail,
        'user_name': username,
        'goods_list': goods_list,
        'explain': explain,
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request, index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(user_id=int(user_id)).order_by('-odate')
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
        user.ushou = request.POST.get('ushou')
        user.uaddress = request.POST.get('uaddress')
        user.uyoubian = request.POST.get('uyoubian')
        user.uphone = request.POST.get('uphone')
        user.save()
    context = {
        'page_name': 1,
        'title': '用户中心',
        'user': user,
    }
    return render(request, 'df_user/user_center_site.html', context)

@user_decorator.login
def revise_info_handle(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        user.uname = request.POST.get('name')
        user.uemail = request.POST.get('uemail')
        user.uphone = request.POST.get('phone')
        user.save()
    context = {
        'page_name': 1,
        'title': '用户中心',
        'user': user,
    }
    return render(request, 'df_user/user_center_info.html', context)


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
    good = GoodsInfo.objects.create(isDelete=isDelete, gtitle=gname, gpic=gpic, gjianjie=gjianjie, gcontent=gcontent,
                                    gtype=typeinfo, gcode=gcode, gdoc=gdoc, guser=user)

    print('user id =', user.id)
    print('good id =', good.id)
    # good = GoodsInfo.objects.get()
    return render(request, 'df_user/user_center_seller.html', None)
    # return render(request, 'df_user/user_center_seller.html', context)


@user_decorator.login
def published(request, index):
    user_id = request.session['user_id']
    print('user id =', user_id)
    goods_list = GoodsInfo.objects.filter(guser=int(user_id)).order_by('-gmdf_time')
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
