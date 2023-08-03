# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class userInfo(models.Model):
    email = models.EmailField(max_length=32, unique=True)
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    ctime = models.DateTimeField(auto_now_add=True)

class sendMsg(models.Model):
    email = models.EmailField(max_length=32, unique=True, db_index=True)
    code = models.CharField(max_length=6)
    firstSendTime = models.DateTimeField()
    tempTimes = models.IntegerField(default=0)


'''
为减少连表，提高效率，
将不变化的数据直接写到数据库表
class kindOfNews(models.Model):
    kindName = models.CharField(max_length=20)
'''

class chouTiNews(models.Model):
    title = models.CharField(max_length=20)
    summary = models.CharField(max_length=200, null=True)
    url = models.URLField(max_length=32, null=True)
    kindName = models.CharField(max_length=20)
    portraitPath = models.CharField(max_length=200)
    authour = models.ForeignKey("userInfo")
    createTime = models.DateTimeField(auto_now_add=True)
    likedCount = models.IntegerField(default=0)
    commentedCount = models.IntegerField(default=0)

class commentSOfNews(models.Model):
    content = models.CharField(max_length=100)
    author = models.ForeignKey(userInfo)
    new    = models.ForeignKey(chouTiNews)
    device = models.CharField(max_length=16, null=True)
    createTime = models.DateTimeField(auto_now_add=True)
    parentComment_id = models.ForeignKey(to="self", related_name="parentCommentTable", null=True)



class usersLikeNews(models.Model):
    user = models.ForeignKey(userInfo)
    new = models.ForeignKey(chouTiNews)

    class Meta:
        unique_together = ("user", "new")
