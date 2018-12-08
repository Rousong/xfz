from django.db import models


class NewsCategory(models.Model):
    name = models.CharField(max_length=10, unique=True, verbose_name='分类名')
    added_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '新闻分类'
        verbose_name_plural = verbose_name


class News(models.Model):
    title = models.CharField(max_length=50, verbose_name='新闻标题')
    desc = models.CharField(max_length=100, verbose_name='新闻描述')
    thumbnail = models.URLField(verbose_name='缩略图')
    content = models.TextField(verbose_name='新闻内容')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    category = models.ForeignKey('NewsCategory', on_delete=models.PROTECT,
                                 null=True, verbose_name='新闻类别')
    author = models.ForeignKey('xfzauth.User', on_delete=models.PROTECT,
                               null=True, verbose_name='新闻作者')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']


class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='评论发布时间')
    news = models.ForeignKey('News', on_delete=models.PROTECT,
                             related_name='comments',
                             verbose_name='评论所属的新闻')
    author = models.ForeignKey('xfzauth.User', on_delete=models.PROTECT,
                               verbose_name='新闻作者')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.content[:10]

    class Meta:
        verbose_name = '新闻评论'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']


class Banner(models.Model):
    priority = models.IntegerField(default=0, verbose_name='轮播图优先级')
    image_url = models.URLField(verbose_name='轮播图图片链接')
    link_to = models.URLField(verbose_name='轮播图跳转链接')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已删除')

    def __str__(self):
        return self.priority

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['-priority']
