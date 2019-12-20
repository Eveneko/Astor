#!/user/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

app_name = 'df_user'

urlpatterns = [
    url(r'^register/$', register, name="register"),
    url(r'^register_handle/$', register_handle, name="register_handle"),
    url(r'^register_exist/$', register_exist, name="register_exist"),
    url(r'^login/$', login, name="login"),
    url(r'^login_handle/$', login_handle, name="login_handle"),
    url(r'^info/$', info, name="info"),
    url(r'^order/(\d+)$', order, name="order"),
    url(r'^site/$', site, name="site"),
    # url(r'^place_order/$', views.place_order),
    url(r'^logout/$', logout, name="logout"),
    url(r'^publish/$', publish, name="publish"),
    url(r'^publish_handle/$', publish_handle, name="publish_handle"),  # 发布算法
    url(r'^published/(\d+)$', published, name="published"),  # 已发布算法
    url(r'^code_runner/$', code_runner, name="code_runner"),
    url(r'^creat_task/$', creat_task, name="creat_task"),
]
