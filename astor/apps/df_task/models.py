from django.db import models
from datetime import datetime

class Task(models.Model):
    creator = models.ForeignKey('df_user.UserInfo',
                                  on_delete=models.CASCADE)
    algorithm = models.ForeignKey('df_goods.GoodsInfo',
                                       on_delete=models.CASCADE)
    # TODO: 使用枚举类型
    status = models.CharField(verbose_name="task_status",
                              max_length=20, default='')
    update_time = models.TimeField(verbose_name='上次修改时间',
                                   default=datetime.now)
    cfg_file = models.FileField(verbose_name='配置模板地址',
                                    upload_to='task/%Y-%m',
                                    null=True, blank=True)
    class Meta:
        verbose_name = "任务信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.task_user.uname)
