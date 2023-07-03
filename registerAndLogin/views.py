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
    print "?????"
    return HttpResponse(stream.getvalue())
