# Generated by Django 2.1.3 on 2018-11-28 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='课程名称')),
                ('video_url', models.URLField(verbose_name='课程地址')),
                ('cover_url', models.URLField(verbose_name='封面图地址')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='课程价格')),
                ('duration', models.IntegerField(verbose_name='课程时长(秒)')),
                ('profile', models.TextField(verbose_name='课程简介')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='课程发布时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='最近修改时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否已删除')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='分类名')),
                ('added_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='最近修改时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否已删除')),
            ],
            options={
                'verbose_name': '课程分类',
                'verbose_name_plural': '课程分类',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='讲师名')),
                ('avatar', models.URLField(verbose_name='讲师头像')),
                ('jobtitle', models.CharField(max_length=20, verbose_name='讲师头衔')),
                ('profile', models.TextField(verbose_name='计量简介')),
                ('added_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='最近修改时间')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否已删除')),
            ],
            options={
                'verbose_name': '讲师',
                'verbose_name_plural': '讲师',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.CourseCategory', verbose_name='课程分类'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.Teacher', verbose_name='课程讲师'),
        ),
    ]