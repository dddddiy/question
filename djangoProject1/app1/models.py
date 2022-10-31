
from django.db import models

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=32)
    #1
    pwd = models.CharField(max_length=64,default="")

