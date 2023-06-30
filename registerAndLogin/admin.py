# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import userInfo, sendMsg

admin.site.register(userInfo)
admin.site.register(sendMsg)
