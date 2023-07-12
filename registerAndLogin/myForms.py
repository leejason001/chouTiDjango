#coding: utf8

from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator


class loginForm(forms.Form):#
    username = fields.CharField(required=True,
                                validators = [RegexValidator(r'^[a-zA-Z0-9_-]+@([a-zA-Z0-9_-]+)(.[a-zA-Z0-9_-]+)+$', u'邮箱格式错误')],
                                error_messages = {
                                    "required": u'此处不能为空'
                                })
    password = fields.CharField(required=True, widget=widgets.PasswordInput, error_messages={"required": u'密码不能为空'})
