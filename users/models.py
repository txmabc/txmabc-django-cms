from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20, verbose_name="登录用户名", unique=True)
    password = models.CharField(max_length=256, verbose_name="加密密码")