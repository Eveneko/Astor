from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import GoodsInfo, TypeInfo
from apps.df_user import user_decorator
from django.urls import reverse
from django.core import serializers
# from df_cart.models import CartInfo
from df_user.models import UserBuyAlgorithm
from django.http.response import JsonResponse
from .forms import LikeForm
from django.core.exceptions import ObjectDoesNotExist, RequestAborted
from django.db import transaction


@user_decorator.login
def index(request):
    """
    商品主页信息，可以获取在售商品信息
    支持指定查找数量，偏移量，按类型查找
    TODO: 支持自定义排序
    API:
    - GET:
        - ^good/{?{query_num=?&}{offset=?&}{type_id=?&}}
            > http://127.0.0.1:8000/good/?type_id=6&query_num=1&offset=1
    :param request: 请求对象
    :return: 渲染页面
    """
    if request.method == 'GET':
        context = {'title': 'Astor'}
        query_num = int(request.GET['query_num']) \
            if 'query_num' in request.GET.keys() else 16
        offset = int(request.GET['offset']) \
            if 'offset' in request.GET.keys() else 0
        type_id = request.GET['type_id'] \
            if 'type_id' in request.GET.keys() else None
        goods_list = GoodsInfo.objects.all()\
            .values('id', 'name', 'type', 'type__name', 'description', 'pic_path')
        if type_id is not None and type_id != '-1':
            good_type = TypeInfo.objects.get(pk=int(type_id))
            goods_list = list(goods_list.filter(type=good_type))
        # return JsonResponse(context)
        context['type_list'] = list(TypeInfo.objects.all().values('id', 'name'))
        context['type_id'] = -1 if type_id is None else int(type_id)
        context['goods_num'] = len(goods_list)
        context['goods_list'] = goods_list[offset:offset+query_num]
        context['like_form'] = LikeForm()
        context['checked_type_id'] = int(type_id) if type_id is not None else -1
        print(context)
        # 添加用户收藏的算法
        try:
            user_like_algorithm_list = UserBuyAlgorithm.objects\
                .all().values('algorithm_id').filter(
                user__id=request.session['user_id'],
            )
            tmp = []
            for a in user_like_algorithm_list:
                tmp.append(int(a['algorithm_id']))
            user_like_algorithm_list = tmp
        except ObjectDoesNotExist:
            user_like_algorithm_list = []
        context['user_like_algorithm_list'] = user_like_algorithm_list
        if request.is_ajax():
            return JsonResponse(context)
        return render(request, 'df_goods/index.html', context)
    elif request.method == 'POST':
        raise Exception('UNSUPPORTED HTTP METHOD')
    else:
        raise Exception('UNSUPPORTED HTTP METHOD')


def detail(request, good_id):
    """
    商品详情页面展示
    API:
    - GET:
        - ^/good/good-{gid}/
            > http://127.0.0.1:8000/good/good-66/
    :param request: 请求对象
    :param good_id: 商品ID
    :return: 渲染页面
    """
    context = {'title': '商品详情'}
    if request.method == 'GET':
        good = GoodsInfo.objects.all()\
            .values('id', 'name', 'description', 'detail', 'cpu_price',
                    'gpu_price', 'pic_path', 'cfg_template',
                    'modify_time', 'type__name')\
            .get(pk=int(good_id))
        context['good'] = good
        try:
            user_like_algorithm_list = UserBuyAlgorithm.objects \
                .all().values('algorithm_id').filter(
                user__id=request.session['user_id'],
            )
            tmp = []
            for a in user_like_algorithm_list:
                tmp.append(int(a['algorithm_id']))
            user_like_algorithm_list = tmp
        except ObjectDoesNotExist:
            user_like_algorithm_list = []
        context['isLiked'] = True if int(good_id) in user_like_algorithm_list else False
        # return JsonResponse(context)
        return render(request, 'df_goods/detail.html', context)
    elif request.method == 'POST':
        raise Exception('UNSUPPORTED HTTP METHOD')
    else:
        raise Exception('UNSUPPORTED HTTP METHOD')


@user_decorator.login
@transaction.atomic
def like(request):
    """
    添加收藏，修改 UserBuyAlgorithm表单
    API：
    - ^/good/like/?good_id={\d}&{like={True|False}
    :param request: 请求实体
    :return: 渲染页面
    """
    if request.method == 'GET':
        # print(request.GET)
        cururl = request.GET.urlencode()
        print(cururl)
        good_id = int(request.GET['good_id'])
        like = str(request.GET['like'])
        red_url = str(request.GET['red_url'])
        if like == 'True':
            like = True
        elif like == 'False':
            like = False
        else:
            raise RequestAborted('UNSUPPORTED ARGUMENT')
        user_id = request.session['user_id']
        user_buy_algorithm = UserBuyAlgorithm.objects.all().filter(user_id=user_id)
        # print(user_buy_algorithm)
        if like:
            if user_buy_algorithm.filter(algorithm_id=good_id).count() == 0:
                UserBuyAlgorithm.objects.create(
                    user_id=user_id,
                    algorithm_id=good_id)
            # print("User {} likes {}".format(user_id, good_id))
        else:
            if user_buy_algorithm.filter(algorithm_id=good_id).count() == 1:
                user_buy_algorithm.get(
                    user_id=user_id,
                    algorithm_id=good_id).delete()
            # print("User {} likes {}".format(user_id, good_id))
        context = {'title': 'Astor'}
        print(red_url)
        # return render(request, 'df_goods/index.html', context)
        return redirect(red_url)

    elif request.method == 'POST' and request.POST:
        # TODO: Using POST to finish like and dislike action
        # print(request.POST)
        # like_form = LikeForm(data=request.POST)
        # like = like_form.clean_like()
        # good_id = like_form.clean_good_id()
        # # user = UserInfo.objects.get(id=request.session['user_id'])
        # user_id = request.session['user_id']
        # if like:
        #     UserBuyAlgorithm.objects.create(
        #         user__id=user_id,
        #         algorithm__id=good_id)
        #     print("User {} likes {}".format(user_id, good_id))
        # else:
        #     UserBuyAlgorithm.objects.get(
        #         user__id=user_id,
        #         algorithm__id=good_id
        #     ).detete()
        # context = {'title': 'Astor'}
        # return render(request, 'df_goods/index.html', context)
        raise Exception('UNSUPPORTED HTTP METHOD')
    else:
        raise Exception('UNSUPPORTED HTTP METHOD')


def ordinary_search(request):
    from django.db.models import Q
    search_keywords = request.GET.get('search', '')
    search_status = 1
    try:
        user_id = request.session['user_id']
    except:
        user_id = None

    print('search_keywords:', search_keywords)

    goods_list = GoodsInfo.objects.filter(
        Q(name__icontains=search_keywords) |
        Q(description__icontains=search_keywords) |
        Q(detail__icontains=search_keywords))

    if goods_list.count() == 0:
        search_status = 0
        goods_list = GoodsInfo.objects.all().order_by("modify_time")[:4]

    context = {
        'title': '搜索列表',
        'search_status': search_status,
        'goods_list': goods_list
    }
    return render(request, 'df_goods/ordinary_search.html', context)
