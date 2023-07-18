# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
import io
import re
import json
import datetime

import myForms
from utils import check_code as CheckCode
from utils import myTools


def _fullmatch(regex, string, flags=0):
    if hasattr(re, 'fullmatch'):
        return re.fullmatch(regex, string)
    return re.match("(?:" + regex + ")\Z", string, flags=flags)

# Create your views here.
def showChouTiIndex(request):
    loginObj = myForms.loginForm()
    return render(request, "chouTiIndex.html", {'loginObj': loginObj})

def getValidateCodeImage(request):
    stream = io.BytesIO()
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())

def loginChouTi(request):
    obj = myForms.loginForm(request.POST)
    if request.POST.get("inputValidateCode") != None and request.POST.get("inputValidateCode").lower() == request.session["CheckCode"].lower():
        if obj.is_valid():
            #在数据库中查询，若有此用户，就可以正常登录，否则登录失败，走后端验证失败的render
            return render( request, "chouTiIndex.html" )
    return render(request, "chouTiIndex.html", {"loginObj":obj})

def submitValidateEmail(request):
    rep = myTools.BaseResponse();
    email = request.POST.get("validateEmail");
    if _fullmatch(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+([\.a-zA-Z0-9_-]+)+', email) == None:
        rep.status = False;
        rep.summary = "邮箱格式错误"
        return HttpResponse(json.dumps(rep.__dict__))

    if models.objects.userInfo.filter(email=email).count() !=0:
        rep.status = False
        rep.summary = "该邮箱已经被注册"
        return HttpResponse(json.dumps(rep.__dict__))

    validationCodeEmailed = myTools.getValidationCode()
    currentTime = datetime.datetime.now()
    if models.objects.sendMsg.filter(email=email).count() == 0:
        models.objects.sendMsg.create(email=email, code=validationCodeEmailed, firstSendTime=currentTime)









    return HttpResponse("ok")

def registerChouTi(request):

    return render(request, "chouTiIndex.html")



