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

from django.utils.safestring import mark_safe
import math


def _fullmatch(regex, string, flags=0):
    if hasattr(re, 'fullmatch'):
        return re.fullmatch(regex, string)
    return re.match("(?:" + regex + ")\Z", string, flags=flags)

def computePageNumbers(pageNumberCount, basePageNum, PAGE_NUMBERS_NOW, newsMaxNumPerPage, totalNumberOfNews):
    limitLength     = math.ceil(pageNumberCount/2.0)
    limitLength_to  = math.floor(pageNumberCount/2.0)
    maxPageNum = math.ceil(float(totalNumberOfNews)/float(newsMaxNumPerPage))

    if basePageNum - limitLength <= 0:
        i = 1
        while i<= pageNumberCount:
            PAGE_NUMBERS_NOW.append(i)
            i += 1
    elif basePageNum + limitLength >= maxPageNum:
        i = 0
        while i<pageNumberCount:
            PAGE_NUMBERS_NOW.append(maxPageNum - i)
            i+=1
            PAGE_NUMBERS_NOW.sort()
    else:
        i=0
        while i<pageNumberCount:
            PAGE_NUMBERS_NOW.append(basePageNum-limitLength_to+i)
            i+=1


# Create your views here.
def showChouTiIndex(request):
    loginObj    = myForms.loginForm()
    registerObj = myForms.registerForm()
    publishWindowObj = myForms.publishWindowForm()


    NEWS_MAX_NUM_PERPAGE = 2
    PAGE_NUMBER_COUNT       = 5
    base_pageNum =  int(request.GET.get("p", 1))
    PAGE_NUMBERS_NOW = []

    computePageNumbers(PAGE_NUMBER_COUNT, base_pageNum, PAGE_NUMBERS_NOW, NEWS_MAX_NUM_PERPAGE, models.chouTiNews.objects.all().count())

    str_pagers = ""
    for pager in PAGE_NUMBERS_NOW:
        pagerHtml = "<a href='/chouTiIndex.html?p=%d'>%d</a>"
        pagerHtml = pagerHtml %(pager, pager)
        str_pagers += pagerHtml

    newsStartIndex = (base_pageNum - 1)*NEWS_MAX_NUM_PERPAGE
    news = models.chouTiNews.objects.all()[newsStartIndex:newsStartIndex+NEWS_MAX_NUM_PERPAGE]

    print str_pagers

    return render(request, "chouTiIndex.html", {'loginObj': loginObj, "registerObj": registerObj, "news": news, "str_pagers": mark_safe(str_pagers), "publishWindowObj": publishWindowObj})

def uploadImage(request):
    portraitObj = request.FILES.get("imageInput")
    import os
    portraitFontPath = os.path.join("font_statics", "upload", portraitObj.name)
    portraitFile = open(os.path.join("statics", "upload", portraitObj.name), "wb")
    for chunk in portraitObj.chunks():
        portraitFile.write(chunk)
    portraitFile.close()
    return HttpResponse(json.dumps({"status":"success", "imagePath":portraitFontPath}))

def upload_aNew(request):
    obj = myForms.publishWindowForm(request.POST)


def getValidateCodeImage(request):
    stream = io.BytesIO()
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())

def loginChouTi(request):
    obj = myForms.loginForm(request.POST)
    # if request.POST.get("inputValidateCode") != None and request.POST.get("inputValidateCode").lower() == request.session["CheckCode"].lower():
    if obj.is_valid():


        value_dict = obj.clean()

        if value_dict["inputValidateCode"].lower() == request.session["CheckCode"].lower():
        #在数据库中查询，若有此用户，就可以正常登录，否则登录失败，走后端验证失败的render
            con1 = Q()
            con1.children.append(('email', value_dict["username"]))
            con1.connector = "AND"
            con1.children.append(('pwd', value_dict["password"]))

            con2 = Q()
            con2.children.append(('username', value_dict["username"]))
            con2.connector = "AND"
            con2.children.append(('pwd', value_dict["password"]))

            con = Q()
            con.add(con1, "OR")
            con.add(con2, "OR")

            obj = models.userInfo.objects.filter(con).first()

            if not obj:
                return render( request, "chouTiIndex.html", {"myErrors": u"用户名邮箱或密码错误"} )
            else:
                request.session['is_login'] = True
                #print obj.id
                request.session['user_info'] = {'id': obj.id, 'email': obj.email, 'username': obj.username}

    return render(request, "chouTiIndex.html", {"loginObj":obj})

def submitValidateEmail(request):
    rep = myTools.BaseResponse()
    email = request.POST.get("validateEmail")
    if _fullmatch(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+([\.a-zA-Z0-9_-]+)+', email) == None:
        rep.status = False
        rep.summary = "邮箱格式错误"
        return HttpResponse(json.dumps(rep.__dict__))

    if models.userInfo.objects.filter(email=email).count() !=0:
        rep.status = False
        rep.summary = "该邮箱已经被注册"
        return HttpResponse(json.dumps(rep.__dict__))

    validationCodeEmailed = myTools.getValidationCode().lower()
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
    print thisValidationTempData
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

def newLikedClick(request):
    user_id = int(request.session.get("user_info")["id"])
    new_id = int(request.POST.get("new_id"))
    newLikedRecord = models.usersLikeNews.objects.filter(Q(user=user_id) and Q(new=new_id))
    if newLikedRecord.count() == 0:
        models.usersLikeNews.objects.create(user=models.userInfo.objects.filter(id=user_id)[0], new=models.chouTiNews.objects.filter(id=new_id)[0])
        models.chouTiNews.objects.filter(id=new_id).update(likedCount=F("likedCount") + 1)
    else:
        newLikedRecord.delete()
        models.chouTiNews.objects.filter(id=new_id).update(likedCount=F("likedCount") - 1)

    return HttpResponse(models.chouTiNews.objects.filter(id=new_id)[0].likedCount)

def getComments(request):
    commentsTable = []
    for comment in models.commentSOfNews.objects.filter(new=int(request.GET.get("new_id"))).values("id", "content", "author", "new", "device", "parentComment_id"):
        commentsTable.append(comment)

    newCommentsTalbe = {}
    for comment in commentsTable:
        comment.update({"children":[]})
        newCommentsTalbe.update({comment["id"]:comment})

    ret = []
    for comment in commentsTable:
        if None == comment["parentComment_id"]:
            ret.append(comment)
        else:
            newCommentsTalbe[comment["parentComment_id"]]["children"].append(comment)


    return HttpResponse(json.dumps(ret))

def submitNewComment(request):
    content = request.POST.get("commentContent")
    author    = models.userInfo.objects.filter(id=request.session.get("user_info")["id"])[0]
    new     = models.chouTiNews.objects.filter(id=int(request.POST.get("new_id")))[0]
    if content and author and new:
        obj = models.commentSOfNews.objects.create(content=content, author=author, new=new)
        return HttpResponse(obj.id)
    else:
        return HttpResponse("failed")

def submitCommentReply(request):
    content = request.POST.get("content")
    author  = models.userInfo.objects.filter(id=request.session.get("user_info")["id"])[0]
    new     = models.chouTiNews.objects.filter(id=int(request.POST.get("new_id")))[0]
    parentComment = models.commentSOfNews.objects.filter(id=int(request.POST.get("parentComment_id")))[0]
    if content and author and new and parentComment:
        obj = models.commentSOfNews.objects.create(content=content, author=author, new=new, parentComment_id=parentComment)
        return HttpResponse(obj.id)
    else:
        return HttpResponse("failed")


