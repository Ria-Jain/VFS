# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Question,Answer,Comment
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from hospital_reg.models import *
from django.contrib.auth import authenticate,login,logout
import smtplib
import re
import hashlib
from email.MIMEMultipart import MIMEMultipart
from hospital_reg.safe import usermail,upassword
from email.MIMEText import MIMEText
import datetime
# Create your views here.

def index(request):
	return render(request,'index.html')

def login(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			return HttpResponse('You are loggedd in')
		else:
			context = {}
			context['error'] = "Wrong Credentials"
			return render(request, 'login.html',context)
	else:
		context = {}
		context['error'] = ''
		return render(request,'login.html', context)

# def logout(request):
# 	if request.user.is_authenticated():
# 		logout(request)
# 		return redirect('/login/')
# 	else:
# 		return HttpResponse('You need to log in')
