# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
import io
from utils import check_code as CheckCode
# Create your views here.
def showChouTiIndex(request):
    return render(request, "chouTiIndex.html")

def getValidateCodeImage(request):
    stream = io.BytesIO()
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())

def loginChouTi(request):
    if request.POST.get("inputValidateCode") != None and request.POST.get("inputValidateCode").lower() == request.session["CheckCode"].lower():
        print "验证通过"
    elif request.POST.get("inputValidateCode") == None:
        print "NNNNN"
    else:
        print "验证失败"
    print request.POST.get("username")

    return render(request, "chouTiIndex.html")
