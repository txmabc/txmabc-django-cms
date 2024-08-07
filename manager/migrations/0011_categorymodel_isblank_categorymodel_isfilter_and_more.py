# Generated by Django 4.2.6 on 2023-11-05 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0010_categorymodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="categorymodel",
            name="isblank",
            field=models.IntegerField(default=0, verbose_name="新窗口"),
        ),
        migrations.AddField(
            model_name="categorymodel",
            name="isfilter",
            field=models.IntegerField(default=0, verbose_name="列表筛选"),
        ),
        migrations.AddField(
            model_name="categorymodel",
            name="isshow",
            field=models.IntegerField(default=0, verbose_name="导航显示"),
        ),
    ]
