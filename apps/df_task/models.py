from df_goods.models import GoodsInfo
from django.db import models
from df_user.models import UserInfo

import datetime


class Task(models.Model):
    task_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE,
                                  verbose_name="task user")  # One task only have one user
    task_algorithm = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE)
    task_data_url = models.CharField(max_length=200, verbose_name="task_data_url")
    task_start_time = models.DateTimeField("task start time", default=datetime.time())
    task_end_time = models.DateTimeField("task end time", default=datetime.time())
    task_status = models.IntegerField(verbose_name="task_status", default=0)  # 0未开始，1进行中，2成功，-1失败
    cpu = models.CharField(max_length=100, verbose_name="cpu", default='1')
    memory = models.CharField(max_length=100, verbose_name="mem", default='128')
    output = models.CharField(max_length=100, verbose_name="out", default='0')

    class Meta:
        verbose_name = "task"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.task_user


'''""
BEGIN;
--
-- Create model Task
--
CREATE TABLE "df_task_task" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "task_data_url" varchar(200) NOT NULL,
    "task_start_time" datetime NOT NULL,
    "task_end_time" datetime NOT NULL, 
    "task_status" integer NOT NULL, 
    "task_algorithm_id" integer NOT NULL REFERENCES "df_goods_goodsinfo" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "task_user_id" integer NOT NULL REFERENCES "df_user_userinfo" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "df_task_task_task_algorithm_id_ce80cf86" ON "df_task_task" ("task_algorithm_id");
CREATE INDEX "df_task_task_task_user_id_d3524eda" ON "df_task_task" ("task_user_id");
COMMIT;
'''