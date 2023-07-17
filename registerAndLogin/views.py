# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
import io
import re

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
    print 22222222222
    print loginObj
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
    email = request.POST.get("validateEmail");
    if _fullmatch(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+([\.a-zA-Z0-9_-]+)+', email) == None:
        return HttpResponse("Email validate failed!")

    print myTools.getValidationCode();


    return HttpResponse("ok")

def registerChouTi(request):

    return render(request, "chouTiIndex.html")



