# Generated by Django 4.2.6 on 2023-12-12 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0028_jobformmodel_islock"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobformmodel",
            name="ordnum",
            field=models.IntegerField(default=0, verbose_name="排序"),
        ),
    ]
