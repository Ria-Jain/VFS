# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Question,Answer, Comment
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import smtplib
import hashlib
import datetime
# Create your views here.

def index(request):
	questions = Question.objects.order_by('created_date')
	context = {
		'questions' : questions
	}
	return render(request,'index.html', context)

def base(request):
	return render(request,'base.html')


def user_profile(request):
	return render(request, 'user_profile.html')

def login_site(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			print(username)
			login(request, user)
			return redirect('/index/')
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
		name = request.POST['name']
		username = request.POST['email']
		password = request.POST['password']
		user = User.objects.create(
				username = username
			)
		user.set_password(password)
		user.save()
		return redirect('/index/')
	else:
		return render(request, 'register.html')

def ask_question(request):
	if request.user.is_authenticated():
		print('Authenticated')
		if request.method == 'POST':
			print('POST request')
			author = request.user
			question_title = request.POST['question_title']
			question_text = request.POST['question_text']
			question = Question.objects.create(
					author=author,
					question_title=question_title,
					question_text=question_text,
				)
			question.save()
			print('Saved')
			return redirect('/index/')
		else:
			print('GET request')
			return render(request, 'ask_question.html')
	else:
		print('Not Authenticated')
		return redirect('/login/')

def question_detail(request, question_id):
	print(request.user.username)
	if request.method == 'POST':
		author = request.user
		question = Question.objects.get(id=question_id)
		text = request.POST['answer']
		ans = Answer.objects.create(
				author=author,
				answer_text=text,
				question=question
			)
		ans.save()
		return redirect('/question_detail/' + str(question_id) + '/')
	else :
		ques = Question.objects.get(id=question_id)
		answers = Answer.objects.filter(question=ques)
		c = []
		for ans in answers:
			c.append(Comment.objects.filter(answer=ans))
		context = {
			'question' : ques,
			'answers' : answers,
			'user' : request.user,
			'comments' : c,
		}
		print(context)
		return render(request, 'question_detail.html', context)


def countUp(request, question_id, answer_id):
	ans = Answer.objects.get(id=answer_id)
	ans.avotes+=1
	ans.save()
	return redirect('/question_detail/' + str(question_id) + '/')

def countDown(request, question_id, answer_id):
	ans = Answer.objects.get(id=answer_id)
	ans.avotes-=1
	ans.save()
	return redirect('/question_detail/' + str(question_id) + '/')
