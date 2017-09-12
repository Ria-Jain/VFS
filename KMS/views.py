# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Question,Answer,Comment
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import smtplib
import hashlib
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
			return render(request, 'index.html')
		else:
			context = {}
			context['error'] = "Wrong Credentials"
			return render(request, 'login.html',context)
	else:
		context = {}
		context['error'] = ''
		return render(request,'login.html', context)

def logout(request):
	if request.user.is_authenticated():
		logout(request)
		return redirect('/login/')
	else:
		return HttpResponse('You need to log in')

def register(request):
	if request.method == 'POST':
		print('Hi')
		name = request.POST['name']
		username = request.POST['email']
		password = request.POST['password']
		print(username)
		user = User.objects.create(
				username = username
			)
		user.set_password(password)
		user.save()
		return redirect('/index/')
	else:
		return render(request, 'register.html')