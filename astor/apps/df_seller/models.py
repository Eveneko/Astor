from django.db import models


# Create your models here.
class SellerInfo(models.Model):
    seller_name = models.CharField(max_length=20, verbose_name="seller_name", unique=True)
    seller_password = models.CharField(max_length=40, verbose_name="seller_password", blank=False)
    seller_email = models.EmailField(verbose_name="email", unique=True)
    seller_phone = models.CharField(max_length=11, default="", verbose_name="seller_phone_number", unique=True)
    seller_payment_account = models.CharField(max_length=20, default="", verbose_name="seller_payment_account",
                                              unique=True)

    # default, blank是python层面的约束，不影响数据库表结构，修改时不需要迁移 python manage.py makemigrations

    class Meta:
        verbose_name = "seller_info"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.seller_name
