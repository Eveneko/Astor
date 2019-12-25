from django.db import models

from datetime import datetime

import uuid


class UserInfo(models.Model):
    uname = models.CharField(max_length=20, verbose_name="用户名", unique=True)
    upwd = models.CharField(max_length=40, verbose_name="用户密码", blank=False)
    uemail = models.EmailField(verbose_name="邮箱", unique=True)
    ushou = models.CharField(max_length=20, default="", verbose_name="收货地址")
    uaddress = models.CharField(max_length=100, default="", verbose_name="地址")
    uyoubian = models.CharField(max_length=6, default="", verbose_name="邮编")
    uphone = models.CharField(max_length=11, default="", verbose_name="手机号")
    # default,blank是python层面的约束，不影响数据库表结构，修改时不需要迁移 python manage.py makemigrations

    user_payment_account = models.CharField(max_length=20, default=uuid.uuid1, verbose_name="user payment account",
                                            unique=True)

    # user_algorihtm_bought = models.ManyToManyField(GoodsInfo)  # 用户已购买的算法，是多对多的关系

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.uname


# class SellerInfo(models.Model):
#     user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户ID")
#     good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="商品ID")
#     last_modify_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

#     class Meta:
#         verbose_name = "卖家信息"
#         verbose_name_plural = verbose_name

#     def __str__(self):
#         return "{0}创建算法商品{1}".format(self.user.uname, self.good.gtitle)

from df_goods.models import GoodsInfo


class GoodsBrowser(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户ID")
    good = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="商品ID")
    browser_time = models.DateTimeField(default=datetime.now, verbose_name="浏览时间")

    class Meta:
        verbose_name = "用户浏览记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}浏览记录{1}".format(self.user.uname, self.good.gtitle)


class UserBuyAlgorithm(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="用户ID")
    algorithm = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE, verbose_name="商品ID")

    class Meta:
        verbose_name = "用户购买的算法"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}购买的算法{1}".format(self.user.uname, self.algorithm.gtitle)
