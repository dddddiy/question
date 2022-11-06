
from django.db import models

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名")
    #1
    pwd = models.CharField(max_length=64,default="",verbose_name="密码")

