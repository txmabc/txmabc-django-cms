# Generated by Django 4.2.6 on 2023-10-27 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0003_alter_admin_pid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="lastlogindate",
            field=models.DateTimeField(auto_now=True, null=True, verbose_name="最后登录日期"),
        ),
    ]
