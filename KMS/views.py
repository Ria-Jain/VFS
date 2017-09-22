# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Question,Answer, Comment, Profile
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import smtplib
import hashlib
import datetime
from django.db.models import Q
# Create your views here.

def index(request):
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	questions_rq = Question.objects.order_by('-created_date')
	answer_rq = []
	for ques in questions_rq:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_rq.append(ans)

	questions_ma = Question.objects.order_by('-numAns')
	answer_ma = []
	for ques in questions_ma:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_ma.append(ans)

	questions_ra = Question.objects.order_by('-recentAnswer')
	answer_ra = []
	for ques in questions_ra:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_ra.append(ans)

	questions_na = Question.objects.filter(numAns=0)
	answer_na = []
	for ques in questions_na:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_na.append(ans)
	context ={
		'questions_all' : questions_all,
		'answers_all' : answer_all,
		'questions_rq' : questions_rq,
		'answers_rq' : answer_rq,
		'questions_ma' : questions_ma,
		'answers_ma' : answer_ma,
		'questions_ra' : questions_ra,
		'answers_ra' : answer_ra,
		'questions_na' : questions_na,
		'answers_na' : answer_na
	}
	return render(request,'index.html', context)

def base(request):
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)
	context = {
		'questions_all' : questions_all,
		'answers_all' : answer_all
	}
	print(context)
	return render(request,'base.html', context)


def user_profile(request):
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	pro_all=Profile.objects.all()
	cuser=[]
	for pro in pro_all:
		if pro.username == request.user.username:
			cuser.append(pro)

	context = {
		'questions_all' : questions_all,
		'answers_all' : answer_all,
		'cuser' : cuser
	}
	return render(request, 'user_profile.html', context)

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

def logout_site(request):
	logout(request)
	return redirect('/index/')

def register(request):
	if request.method == 'POST':
		firstName = request.POST['fname']
		lastName = request.POST['lname']
		username = request.POST['email']
		password = request.POST['password']
		user = User.objects.create(
				username = username,
				first_name = firstName,
				last_name = lastName
			)
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/index/')
	else:
		return render(request, 'register.html')

def ask_question(request):
	if request.user.is_authenticated():
		print('Authenticated')
		questions_all = Question.objects.all()
		answer_all = []
		for ques in questions_all:
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_all.append(ans)

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
			context = {
				'questions_all' : questions_all,
				'answers_all' : answer_all
			}
			print('GET request')
			return render(request, 'ask_question.html', context)
	else:
		print('Not Authenticated')
		return redirect('/login/')
def count(request):
	return render(request, 'count.html')

def question_detail(request, question_id):
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)
	if request.method == 'POST':
		if request.user.is_authenticated():
			if 'answer-submit' in request.POST:
				author = request.user
				question = Question.objects.get(id=question_id)
				text = request.POST['answer']
				question.numAns+=1
				question.recentAnswer=timezone.now()
				ans = Answer.objects.create(
						author=author,
						answer_text=text,
						question=question
					)
				question.save()
				ans.save()
			else:
				for key in request.POST:
					print(key)
				author=request.user
				answer=Answer.objects.get(id=key)
				text=request.POST['comment']
				question=Question.objects.get(id=question_id)
				com = Comment.objects.create(
						author=author,
						comment_text=text,
						answer=answer,
						question=question
					)
				com.save()
		else:
			context={}
			context['error'] = 'You need to log in first.'
			return render(request,'login.html',context)


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
			'questions_all' : questions_all,
			'answers_all' : answer_all
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

def edit(request):
	if request.method == 'POST':
		user=User.objects.get(id=request.user.id)
		fname=request.POST['fname']
		lname=request.POST['lname']
		username=request.user.username
		country=request.POST['country']
		website=request.POST['website']
		about=request.POST['about']
		phone=request.POST['phone']

		pro_all=Profile.objects.all()
		for pro in pro_all:
			if pro.username == username:
				flag=1
				pro.firstName=fname
				pro.lastName=lname
				pro.country=country
				pro.website=website
				pro.aboutYourself=about
				pro.phone=phone
				break
		if flag !=1:
			pro=Profile.objects.create(
					user=user,
					firstName=fname,
					lastName=lname,
					username=username,
					country=country,
					website=website,
					aboutYourself=about,
					phone=phone,
					regDate=timezone.now()
				)
		pro.save()
		user.first_name=fname
		user.last_name=lname
		user.username=username
		user.save()
		print('Hi')
		return redirect('/profile/')
	else:
		questions_all = Question.objects.all()
		answer_all = []
		for ques in questions_all:
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_all.append(ans)
		pro_all = Profile.objects.all()
		cuser= []
		for pro in pro_all:
			if pro.username == request.user.username:
				cuser.append(pro)

		context = {
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'cuser' : cuser
		}
		return render(request, 'edit_profile.html', context)

def search(request):
	if request.method == 'POST':
		s = request.POST['question_title']
		querywords = s.split()	#Who is Foo-Bar
		stopwords = ['what','who','is','a','at','is','he']
		result = []
		for word in querywords:
			if word.lower() not in stopwords:
				result.append(word)
		query = Q()
		for word in result:
			query = query | Q(question_title__contains=word) | Q(question_text__contains=word)
			questions = Question.objects.filter(query)
			# questions.append(Question.objects.filter(
			# 		question__Question_title__contains=word
			# 	)
			# )
		print(len(questions))
		context = {
			'questions' : questions
		}
		return render(request, 'search.html', context)
	else:
		return HttpResponse('What?')