#!/user/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'df_cart'

urlpatterns = [
    url(r'^$', views.index, name="cart"),
    url(r'^add(\d+)_(\d+)/$', views.add, name="add"),
    url(r'^edit(\d+)_(\d+)/$', views.edit, name="edit"),
    url(r'^delete(\d+)/$', views.delete, name="delete"),
]
