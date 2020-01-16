# superuser: root 123123...
from django.contrib import admin
from .models import TypeInfo, GoodsInfo


# 注册模型类  普通方法
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_per_page = 10
    search_fields = ['name']
    list_display_links = ['name']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'name', 'type', 'cpu_price', 'gpu_price', 'pic_path',
                    'description', 'detail', 'cfg_template']
    search_fields = ['name', 'type']
    list_display_links = ['name']


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
