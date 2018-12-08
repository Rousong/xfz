from django.db import models
from shortuuidfield import ShortUUIDField


class CourseCategory(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='分类名')
    added_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    username = models.CharField(max_length=20, verbose_name='讲师名')
    avatar = models.URLField(verbose_name='讲师头像')
    jobtitle = models.CharField(max_length=20, verbose_name='讲师头衔')
    profile = models.TextField(verbose_name='计量简介')
    added_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '讲师'
        verbose_name_plural = verbose_name


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='课程名称')
    category = models.ForeignKey('CourseCategory', on_delete=models.PROTECT,
                                 verbose_name='课程分类')
    teacher = models.ForeignKey('Teacher', on_delete=models.PROTECT,
                                verbose_name='课程讲师')
    video_url = models.URLField(verbose_name='课程地址')
    cover_url = models.URLField(verbose_name='封面图地址')
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                verbose_name='课程价格')
    duration = models.IntegerField(verbose_name='课程时长(秒)')
    profile = models.TextField(verbose_name='课程简介')
    pub_time = models.DateTimeField(auto_now_add=True,
                                    verbose_name='课程发布时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name


class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True, verbose_name='主键')
    course = models.ForeignKey('Course', on_delete=models.PROTECT,
                               verbose_name='课程')
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
        return f'{self.course} - {self.buyer}'

    class Meta:
        verbose_name = '课程订单表'
        verbose_name_plural = verbose_name
