from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

from .models import *
from apps.df_user import user_decorator
from django.core.exceptions import ObjectDoesNotExist, RequestAborted


@user_decorator.login
def index(request):
    """
    购物车主页
    API:
    - GET
        - ^/cart/
            > http://127.0.0.1:8000/cart/
    :param request: 请求对象
    :return: 渲染网页
    """
    context = {'title': '购物车'}
    if request.method == 'GET':
        uid = request.session['user_id']
        try:
            carts = CartInfo.objects.all()\
                .values('user__uname', 'goods__id', 'goods__name',
                        'goods__type', 'goods__description',
                        'goods__pic_path')\
                .get(user_id=uid)
        except ObjectDoesNotExist:
            carts = []
        context['count'] = len(carts)
        context['carts'] = carts
        if request.is_ajax():
            return JsonResponse(context)
        else:
            return JsonResponse(context)
            # return render(request, 'df_cart/cart.html', context)
    elif request.method == 'POST':
        raise RequestAborted('UNSUPPORTED HTTP METHOD')
    else:
        raise RequestAborted('UNSUPPORTED HTTP METHOD')


@user_decorator.login
def add(request, gid, count):
    # TODO: 使用POST请求+表单验证方式完成用户交互
    uid = request.session['user_id']
    gid, count = int(gid), int(count)
    # 查询购物车中是否已经有此商品，如果有则数量增加，如果没有则新增
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    # 如果是ajax提交则直接返回json，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        # 求当前用户购买了几件商品
        return JsonResponse({'count': count})
    else:
        return redirect(reverse("df_cart:cart"))


@user_decorator.login
def edit(request, cart_id, count):
    # TODO: 使用POST请求+表单验证方式完成用户交互
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        cart.save()
        data['count'] = 0
    except Exception:
        data['count'] = count
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    # TODO: 使用POST请求+表单验证方式完成用户交互
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data['ok'] = 1
    except Exception:
        data['ok'] = 0
    return JsonResponse(data)
