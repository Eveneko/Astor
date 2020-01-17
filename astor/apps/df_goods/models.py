from datetime import datetime
from django.db import models


class TypeInfo(models.Model):
    isDelete = models.BooleanField(default=False)
    name = models.CharField(max_length=20, verbose_name="分类")

    class Meta:
        verbose_name = "商品类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsInfo(models.Model):
    # 具体商品信息
    isDelete = models.BooleanField(default=False)
    name = models.CharField(max_length=20, verbose_name="商品名称")
    pic_path = models.ImageField(upload_to="df_goods/image/%Y/%m",
                                 verbose_name="图片地址",
                                 default="images/default.png")
    cpu_price = models.DecimalField(max_digits=5, decimal_places=2,
                                    verbose_name="CPU核心小时单价", default=0)
    gpu_price = models.DecimalField(max_digits=5, decimal_places=2,
                                    verbose_name="GPU核心小时单价", default=0)
    description = models.CharField(max_length=200, verbose_name="商品简介")
    detail = models.CharField(max_length=1000, verbose_name="商品详情")
    cfg_template = models.FileField(verbose_name='配置模板地址',
                                       upload_to='config/%Y-%m',
                                       null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='算法上市时间',
                                       default=datetime.now)
    modify_time = models.DateTimeField(verbose_name="最近更新时间",
                                       default=datetime.now)
    type = models.ForeignKey(TypeInfo, on_delete=models.CASCADE,
                             verbose_name="分类")

    class Meta:
        verbose_name = "商品信息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
