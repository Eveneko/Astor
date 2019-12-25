from django.contrib import admin

from .models import UserInfo, GoodsBrowser, UserBuyAlgorithm, UserFile


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ["uname", "uemail", "ushou", "uaddress", "uyoubian", "uphone"]
    list_per_page = 5
    list_filter = ["uname", "uyoubian"]
    search_fields = ["uname", "uyoubian"]
    readonly_fields = ["uname"]


class GoodsBrowserAdmin(admin.ModelAdmin):
    list_display = ["user", "good"]
    list_per_page = 50
    list_filter = ["user__uname", "good__gtitle"]
    search_fields = ["user__uname", "good__gtitle"]
    readonly_fields = ["user", "good"]
    refresh_times = [3, 5]


# class SellerInfoAdmin(admin.ModelAdmin):
#     list_display = ["user", "good"]
#     list_per_page = 50
#     list_filter = ["user__uname", "good__gtitle"]
#     search_fields = ["user__uname", "good__gtitle"]
#     readonly_fields = ["user", "good"]
#     refresh_times = [3, 5]

class UserFileAdmin(admin.ModelAdmin):
    list_display = ["user", "file_name", 'file_uuid']
    list_per_page = 50
    list_filter = ["user__uname", "file_name", "file_uuid"]
    search_fields = ["user__uname", "file_name", "file_uuid"]
    # readonly_fields = ["user", "file_name", 'file_uuid']
    refresh_times = [3, 5]


class UserBuyAlgorithmAdmin(admin.ModelAdmin):
    list_display = ["user", "algorithm"]
    list_per_page = 50
    list_filter = ["user__uname", "algorithm__gtitle"]
    search_fields = ["user__uname", "algorithm__gtitle"]
    # readonly_fields = ["user", "algorithm"]
    refresh_times = [3, 5]


admin.site.site_header = 'Astor后台管理系统'
admin.site.site_title = 'Astor后台管理系统'

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(GoodsBrowser, GoodsBrowserAdmin)
# admin.site.register(SellerInfo, SellerInfoAdmin)

admin.site.register(UserBuyAlgorithm, UserBuyAlgorithmAdmin)
admin.site.register(UserFile, UserFileAdmin)
