from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["task_user", "task_algorithm", "task_start_time", "task_end_time", "task_data_url"]
    list_per_page = 50
    list_filter = ["task_user__uname", "task_algorithm__gtitle"]
    search_fields = ["task_user__uname", "task_algorithm__gtitle"]
    # readonly_fields = ["task_user", "task_algorithm"]
    refresh_times = [3, 5]


# Register your models here.
admin.site.register(Task, TaskAdmin)
