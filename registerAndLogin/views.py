# -*- coding: utf-8 -*-
'''

'''

from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
import io
import re
import json
import datetime
from django.db.models import F, Q

import myForms
import models
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
    email = request.POST.get("validateEmail")
    if _fullmatch(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+([\.a-zA-Z0-9_-]+)+', email) == None:
        rep.status = False;
        rep.summary = "邮箱格式错误"
        return HttpResponse(json.dumps(rep.__dict__))

    if models.userInfo.objects.filter(email=email).count() !=0:
        rep.status = False
        rep.summary = "该邮箱已经被注册"
        return HttpResponse(json.dumps(rep.__dict__))

    validationCodeEmailed = myTools.getValidationCode()
    currentTime = datetime.datetime.now()
    if models.sendMsg.objects.filter(email=email).count() == 0:
        models.sendMsg.objects.create(email=email, code=validationCodeEmailed, firstSendTime=currentTime, tempTimes=0)
        rep.status = True
    else:
        limit_oneTime = currentTime - datetime.timedelta(hours=1)

        if models.sendMsg.objects.filter(email=email, firstSendTime__gte=limit_oneTime, tempTimes__gt=9).count():
            rep.status = False;
            rep.summary = "已到发送验证码次数上限，请1小时后再尝试！"
            return HttpResponse( json.dumps( rep.__dict__ ) )
        else:
            models.sendMsg.objects.filter(email=email).update(code=validationCodeEmailed, firstSendTime=currentTime, tempTimes=F("tempTimes")+1)
            rep.status = True

    print validationCodeEmailed
    #myTools.sendEmail(email, validationCodeEmailed)

    return HttpResponse(json.dumps(rep.__dict__))

def registerChouTi(request):
    email = request.POST.get( "validateEmail" )
    validationCode = request.POST.get("validationCode").lower()

    thisValidationTempData = models.sendMsg.objects.filter(email=email, code=validationCode)
    if thisValidationTempData.count():
        if models.userInfo.objects.filter(email=email).count():
            print u"该邮箱已被注册"
            return redirect("chouTiIndex.html")
        else:
            models.userInfo.objects.create(
                email=email,
                username=request.POST.get("username"),
                pwd=request.POST.get("password"),
                ctime=datetime.datetime.now()
            )
            thisValidationTempData.delete()
    else:
        print "ssssssssssss"
    return redirect("chouTiIndex.html")



