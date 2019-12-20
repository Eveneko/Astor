* 尚未实现在数据库中: vip 
* seller 只见了一张表，尚未与goods（算法）在数据库中建立联系


### df_user
####add the following field: 
#####Table UserInfo
    user_payment_account = models.CharField(max_length=20, default=uuid.uuid1, verbose_name="user payment account",unique=True)
    user_algorihtm_bought = models.ManyToManyField(GoodsInfo)  # 用户已购买的算法，是多对多的关系

### df_seller
    new create
### df_task
    new create
    
###df_goods
####add the following field: 
#####Table GoodsInfo
    algorithm_sale_count = models.IntegerField(verbose_name="sale_count", default=0)  # 算法销售量
    algorithm_code_url = models.CharField(max_length=200, verbose_name="algorithm_code_url", default="")
    algorithm_document_url = models.CharField(max_length=200, verbose_name="algorithm_document_url", default="")
    algorithm_status = models.IntegerField(default=0)  # 1,0,-1 #Running,Suspending,Expire…
    algorithm_market_time = models.DateTimeField(default=datetime.now)  # 此算法上市时间
    
###df_order
####add the following field: 
#####Table OrderInfo
    opay_time = models.DateTimeField(verbose_name="支付时间", default=datetime.now)  # 这里应该是支付时间
    