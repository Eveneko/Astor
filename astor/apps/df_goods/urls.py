from django.conf.urls import url

from . import views

app_name = 'df_goods'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^good-(\d+)/$', views.detail, name="detail"),
    url(r'^like/$', views.like, name='like'),
    url(r'^search/', views.ordinary_search, name="ordinary_search"),  # 全文检索
]
