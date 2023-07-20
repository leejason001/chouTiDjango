#coding: utf8

from django import forms
from django.forms import fields
from django.forms import widgets
from django.core.validators import RegexValidator


class loginForm(forms.Form):#
    username = fields.CharField(
        required=True,
        error_messages={"required": u'此处不能为空'},
        widget=widgets.TextInput(
        attrs={"placeholder": u"请输入用户名或邮箱"},
                                ))
    password = fields.CharField(required=True, widget=widgets.PasswordInput(attrs={'placeholder': u'请输入密码'}))
    inputValidateCode = fields.CharField(
        required=True,
        max_length=6,
        widget=widgets.TextInput(
            attrs={"placeholder": u"请输入验证码","class":"validateInput"}
        ))

class registerForm(forms.Form):
    validateEmail = fields.CharField(
        required=True,
        validators=[RegexValidator( r'^[a-zA-Z0-9_-]+@([a-zA-Z0-9_-]+)(\.[a-zA-Z0-9_-]+)+$', u'邮箱格式错误' )],
        error_messages={"required": u'此处不能为空'},
        widget=widgets.TextInput(
        attrs={"placeholder": u"请输入邮箱地址", "class": "validateEmail"},
                                ))

    username = fields.CharField(
        required=True,
        error_messages={"required": u'此处不能为空'},
        widget=widgets.TextInput({"placeholder": u"请输入用户名"}),
    )
