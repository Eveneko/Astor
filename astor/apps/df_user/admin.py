from django.contrib import admin

from .models import UserInfo, UserBuyAlgorithm


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["uname", "uemail"]
    list_per_page = 5
    list_filter = ["uname"]
    search_fields = ["uname", "uemail"]
    # readonly_fields = ["uname"]


class UserBuyAlgorithmAdmin(admin.ModelAdmin):
    list_display = ["user", "algorithm"]
    list_per_page = 50
    list_filter = ["user__uname", "algorithm__name"]
    search_fields = ["user__uname", "algorithm__name"]
    # readonly_fields = ["user", "algorithm"]
    refresh_times = [3, 5]


admin.site.site_header = 'Astor后台管理系统'
admin.site.site_title = 'Astor后台管理系统'

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserBuyAlgorithm, UserBuyAlgorithmAdmin)
