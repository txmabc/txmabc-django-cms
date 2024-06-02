# Generated by Django 4.2.6 on 2023-12-12 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0029_jobformmodel_ordnum"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookModel",
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
                ("truename", models.CharField(max_length=50, verbose_name="姓名")),
                ("tel", models.CharField(max_length=20, verbose_name="座机")),
                ("mobile", models.CharField(max_length=11, verbose_name="手机")),
                ("remark", models.TextField(verbose_name="留言")),
                ("reply", models.TextField(verbose_name="回复")),
                ("islock", models.IntegerField(default=0, verbose_name="状态")),
                ("ontop", models.IntegerField(default=0, verbose_name="置顶")),
                ("createdate", models.IntegerField(default=0, verbose_name="创建时间")),
                ("postip", models.CharField(max_length=20, verbose_name="座机")),
                ("replydate", models.IntegerField(default=0, verbose_name="回复时间")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
