"""chouTiDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from registerAndLogin import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chouTiIndex.html$', views.showChouTiIndex),
    url(r'^login.html$', views.loginChouTi),
    url(r'^getValidateCodeImage/$', views.getValidateCodeImage),
    url(r'^register.html$', views.registerChouTi),
    url(r'^submitValidateEmail$', views.submitValidateEmail),
    url(r'^newLikedClick', views.newLikedClick),
    url(r'^getComments/$', views.getComments),
    url(r'^submitNewComment/', views.submitNewComment),
    url(r'^submitCommentReply/', views.submitCommentReply),
    url(r'^uploadImage.html$', views.uploadImage),
    url(r'^upload_aNew.html$', views.upload_aNew),
]
