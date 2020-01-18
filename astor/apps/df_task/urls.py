#!/user/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

app_name = 'df_task'

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^creat_task/$', creat_task, name="creat_task"),
    url(r'^task_record/$', task_record, name="task_record"),
    url(r'^upload_data/$', upload_data, name="upload_data"),
    # url(r'^upload_file/$', upload_file, name="upload_file"),
    # url(r'^upload_task_config/$', upload_task_config, name="upload_task_config"),
    url(r'^start_task/$', start_task, name="start_task"),
    url(r'^upload_config/$', upload_config, name="upload_config"),
]
