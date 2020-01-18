from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["creator", "algorithm", 'status', 'update_time']
    list_per_page = 50
    list_filter = ["creator__uname", "algorithm__name"]
    search_fields = ["creator__uname", "algorithm__name"]
    refresh_times = [3, 5]
    readonly_fields = ['config']


# Register your models here.
admin.site.register(Task, TaskAdmin)
