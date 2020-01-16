from datetime import datetime
from django.db import models
from tinymce.models import HTMLField  # 使用富文本编辑框要在settings文件中安装


class TypeInfo(models.Model):
    isDelete = models.BooleanField(default=False)
    ttitle = models.CharField(max_length=20, verbose_name="分类")

    class Meta:
        verbose_name = "商品类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    # 具体商品信息
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    gtitle = models.CharField(max_length=20, verbose_name="商品名称")
    gpic = models.ImageField(verbose_name='商品图片', upload_to='image/%Y-%m', null=True, blank=True)  # 商品图片
    gpic = models.ImageField(upload_to="df_goods/image/%Y/%m", verbose_name="图片路径", default="image/default.png")
    gprice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="商品价格", default=0)  # 商品价格小数位为两位，整数位为3位
    gclick = models.IntegerField(verbose_name="点击量", default=0, null=False)
    gjianjie = models.CharField(max_length=200, verbose_name="简介")
    gcontent = HTMLField(max_length=5000, verbose_name="详情")
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE, verbose_name="分类")  # 外键关联TypeInfo表
    # gadv = models.BooleanField(default=False) #商品是否推荐
    gsale = models.IntegerField(verbose_name="销售量", default=0)  # 算法销售量
    gcode = models.FileField(verbose_name='算法代码', upload_to='code/%Y-%m', null=True, blank=True)
    gdoc = models.FileField(verbose_name="文档链接", upload_to='doc/%Y-%m', null=True, blank=True)
    gstatus = models.IntegerField(default=0)  # 1,0,-1         # Running, Suspending, Expire…
    algorithm_market_time = models.DateTimeField(default=datetime.now)  # 此算法上市时间
    gmdf_time = models.DateTimeField(default=datetime.now, verbose_name="修改时间")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.gtitle
