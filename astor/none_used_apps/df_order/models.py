from django.db import models
from datetime import  datetime

class OrderInfo(models.Model):
    id = models.CharField(max_length=20, primary_key=True,
                          verbose_name="订单号")
    user = models.ForeignKey('df_user.UserInfo', on_delete=models.CASCADE,
                             verbose_name="订单用户")
    create_date = models.DateTimeField(auto_now=True,
                                       verbose_name="创建时间")
    is_paid = models.BooleanField(default=False, verbose_name="是否支付")
    oaddress = models.CharField(max_length=150, verbose_name="订单地址")
    # 虽然订单总价可以由多个商品的单价以及数量求得，但是由于用户订单的总价的大量使用，忽略total的冗余度
    opay_time = models.DateTimeField(verbose_name="支付时间",
                                     default=datetime.now)  # 这里应该是支付时间

    class Meta:
        verbose_name = "订单信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}在的订单{1}".format(self.user.uname, self.odate)


# 无法实现：真实支付，物流信息
class OrderDetailInfo(models.Model):  # 大订单中的具体某一商品订单

    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE, verbose_name="商品")  # 关联商品信息
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="商品价格")
    count = models.IntegerField(verbose_name="商品数")

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.goods.gtitle + "(数量为" + str(self.count)  + ")"
        return "{0}(数量为{1})".format(self.goods.gtitle, self.count)