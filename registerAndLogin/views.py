# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
import io

import myForms
from utils import check_code as CheckCode
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
            return render( request, "chouTiIndex.html" )
    return render(request, "chouTiIndex.html", {"loginObj":obj})



