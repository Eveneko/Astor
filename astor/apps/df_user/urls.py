#!/user/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

app_name = 'df_user'


urlpatterns = [
    url(r'^register/$', register, name="register"),
    url(r'^login/$', login, name="login"),
    url(r'^info/$', info, name="info"),
    # url(r'^order/(\d+)$', order, name="order"),
    # url(r'^site/$', site, name="site"),
    # url(r'^place_order/$', views.place_order),
    url(r'^logout/$', logout, name="logout"),
    # url(r'^publish/$', publish, name="publish"),
    # url(r'^publish_handle/$', publish_handle, name="publish_handle"),  # 发布算法
    # url(r'^published/(\d+)$', published, name="published"),  # 已发布算法
    url(r'^revise_info_handle/$', revise_info_handle, name="revise_info_handle"),
    url(r'^my_algorithm', my_algorithm, name="my_algorithm")
]
