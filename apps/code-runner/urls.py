#!/user/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

app_name = 'code-runer'

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^creat_task/$', creat_task, name="creat_task"),
    url(r'^task_record/$', task_record, name="task_record"),
]
