# Generated by Django 4.2.6 on 2023-10-26 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="islock",
            field=models.IntegerField(default=0, verbose_name="状态"),
        ),
        migrations.AlterField(
            model_name="admin",
            name="logintimes",
            field=models.IntegerField(default=0, verbose_name="登录次数"),
        ),
        migrations.AlterField(
            model_name="admin",
            name="readonly",
            field=models.SmallIntegerField(default=0, verbose_name="是否只读"),
        ),
        migrations.AlterField(
            model_name="adminloginlog",
            name="loginstate",
            field=models.SmallIntegerField(null=True, verbose_name="状态"),
        ),
        migrations.AlterField(
            model_name="adminmenu",
            name="followid",
            field=models.IntegerField(default=0, verbose_name="父级"),
        ),
        migrations.AlterField(
            model_name="adminmenu",
            name="islock",
            field=models.IntegerField(default=0, verbose_name="状态"),
        ),
        migrations.AlterField(
            model_name="adminmenu",
            name="ordnum",
            field=models.IntegerField(default=0, verbose_name="菜单排序"),
        ),
        migrations.AlterField(
            model_name="adminpart",
            name="ordnum",
            field=models.IntegerField(default=0, verbose_name="排序"),
        ),
        migrations.AlterField(
            model_name="adminpart",
            name="pagelock",
            field=models.SmallIntegerField(default=0, verbose_name="审核设置"),
        ),
    ]
