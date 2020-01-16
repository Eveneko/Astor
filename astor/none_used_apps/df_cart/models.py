from django.db import models

class CartInfo(models.Model):

    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE,
                             verbose_name="用户")
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE,
                              verbose_name="商品")
    count = models.IntegerField(verbose_name="", default=0)

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.uname + '的购物车'
