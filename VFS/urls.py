"""VFS URL Configuration

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
from KMS import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^base/$', views.base),
    url(r'^login/$', views.login_site),
    url(r'^logout/$', views.logout_site),
    url(r'^register/$', views.register),
    url(r'^edit/$', views.edit),
    url(r'^search/$', views.search),
    url(r'^ask_question/$', views.ask_question),
    url(r'^profile/$', views.user_profile),
    url(r'^search/$', views.search),
    url(r'^countDown/(?P<answer_id>\d+)$', views.countDown),
    url(r'^question_detail/(?P<question_id>\d+)/$', views.question_detail),
    url(r'^viewprofile/(?P<user_id>\d+)/$', views.viewprofile),

    url(r'^countUp/(?P<answer_id>\d+)$', views.countUp),
    url(r'^reply_ajax/(?P<question_id>\d+)/$', views.reply_ajax),
]