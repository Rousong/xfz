# Generated by Django 2.1.3 on 2018-12-03 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payinfo', '0002_payinfoorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payinfoorder',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '未支付'), (2, '支付成功')], default=1, verbose_name='订单状态'),
        ),
    ]
