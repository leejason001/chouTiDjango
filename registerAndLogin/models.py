# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class userInfo(models.Model):
    username = models.CharField(max_length=32, db_index=True)
    email = models.EmailField(max_length=32, unique=True)
    pwd = models.CharField(max_length=32)
    ctime = models.DateTimeField(auto_now_add=True)

class sendMsg(models.Model):
    email = models.EmailField(max_length=32, unique=True, db_index=True)
    code = models.CharField(max_length=6)
    firstSendTime = models.DateTimeField()
    timesLimit = models.IntegerField(default=0)

