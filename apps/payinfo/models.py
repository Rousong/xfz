from django.db import models
from shortuuidfield import ShortUUIDField


class Payinfo(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    profile = models.CharField(max_length=100, verbose_name='简介')
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                verbose_name='价格')
    path = models.FilePathField(verbose_name='存储路径')
    pub_time = models.DateTimeField(auto_now_add=True,
                                    verbose_name='发布时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '付费资讯'
        verbose_name_plural = verbose_name


class PayinfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True, verbose_name='主键')
    payinfo = models.ForeignKey('Payinfo', on_delete=models.PROTECT,
            verbose_name='付费资讯')
    buyer = models.ForeignKey('xfzauth.User', on_delete=models.PROTECT,
                              verbose_name='用户')
    amount = models.DecimalField(max_digits=11, decimal_places=2, default=0,
                                 verbose_name='订单金额')
    pub_time = models.DateTimeField(auto_now_add=True,
                                    verbose_name='订单生成时间')
    istype = models.SmallIntegerField(
            verbose_name='支付类型', default=0,
            choices=((0, '未知'), (1, '支付宝'), (2, '微信')))
    status = models.SmallIntegerField(
            verbose_name='订单状态', default=1, choices=((1, '未支付'), (2, '支付成功')))
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return f'{self.payinfo} - {self.buyer}'

    class Meta:
        verbose_name = '付费资讯订单表'
        verbose_name_plural = verbose_name
