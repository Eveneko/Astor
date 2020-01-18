from django.db import models
from datetime import datetime
from time import time

class Task(models.Model):
    creator = models.ForeignKey('df_user.UserInfo',
                                  on_delete=models.CASCADE)
    algorithm = models.ForeignKey('df_goods.GoodsInfo',
                                       on_delete=models.CASCADE)
    # TODO: 使用枚举类型
    status = models.CharField(verbose_name="task_status",
                              max_length=20, default='')
    update_time = models.DateTimeField(verbose_name='上次修改时间',
                                   auto_now=True)
    config = models.CharField(verbose_name='配置模板',
                                max_length=10000, default='')
    class Meta:
        verbose_name = "任务信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.creator.uname)
