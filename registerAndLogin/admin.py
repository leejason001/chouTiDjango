# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(userInfo)
admin.site.register(sendMsg)
admin.site.register(chouTiNews)
admin.site.register(usersLikeNews)
admin.site.register(commentSOfNews)
