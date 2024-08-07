# Generated by Django 4.2.6 on 2023-12-13 13:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0030_bookmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkModel",
            fields=[
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("webname", models.CharField(max_length=50, verbose_name="网站名称")),
                ("weblogo", models.CharField(max_length=255, verbose_name="网站LOGO")),
                ("weburl", models.CharField(max_length=255, verbose_name="网址")),
                ("islogo", models.IntegerField(default=0, verbose_name="islogo")),
                ("classid", models.IntegerField(default=0, verbose_name="类别")),
                ("ordnum", models.IntegerField(default=0, verbose_name="排序")),
                ("islock", models.IntegerField(default=0, verbose_name="状态")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="bookmodel",
            name="createdate",
            field=models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
        ),
        migrations.AlterField(
            model_name="bookmodel",
            name="replydate",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="回复时间"
            ),
        ),
    ]
