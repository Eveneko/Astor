from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20, verbose_name="用户名", unique=True)
    upwd = models.CharField(max_length=40, verbose_name="用户密码", blank=False)
    uemail = models.EmailField(verbose_name="邮箱", unique=True)

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.uname


class UserBuyAlgorithm(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE,
                             verbose_name="用户ID")
    algorithm = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE,
                                  verbose_name="商品ID")

    class Meta:
        verbose_name = "用户购买的算法"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}购买的算法{1}".format(self.user.uname, self.algorithm.gtitle)


# TODO: 创建新的任务模型并以外键和用户关联
class UserCreateTask(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE,
                             verbose_name="用户ID")
    task_name = models.CharField(max_length=50, verbose_name="创建任务名")
    config_context = models.TextField(verbose_name='用户创建的任务配置信息')
    # TODO: 使用枚举类型
    task_status = models.CharField(max_length=50, verbose_name="任务状态")
    last_update = models.TimeField(verbose_name='算法状态更新时间')

# class UserUploadFile(models.Model):
#     user = models.ForeignKey(UserInfo, on_delete=models.CASCADE,
#                              verbose_name="用户ID")
#     file_name = models.CharField(max_length=50, verbose_name="用户文件名")
#     file_uuid = models.CharField(max_length=100, verbose_name="文件uuid")
#
#     class Meta:
#         verbose_name = "用户上传文件表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "{0},{1}".format(self.file_name, self.file_uuid)

# class GoodsBrowser(models.Model):
#     user = models.ForeignKey(UserInfo, on_delete=models.CASCADE,
#                              verbose_name="用户")
#     good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE,
#                              verbose_name="商品ID")
#     browser_time = models.DateTimeField(default=datetime.now,
#                                         verbose_name="浏览时间")
#
#     class Meta:
#         verbose_name = "用户浏览记录表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return "{0}浏览记录{1}".format(self.user.uname, self.good.gtitle)
