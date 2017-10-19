# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Question,Answer, Comment, Profile, Vote, Tag
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from nltk.corpus import stopwords
import datetime
from django.db.models import Q
import json
import urllib
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.storage import FileSystemStorage
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
	users_rq=[]
	for ques in questions_rq:
		user=Profile.objects.filter(user=ques.author)
		users_rq.append(user)
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_rq.append(ans)

	questions_ma = Question.objects.order_by('-numAns')
	answer_ma = []
	users_ma=[]
	for ques in questions_ma:
		user = Profile.objects.filter(user=ques.author)
		users_ma.append(user)
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_ma.append(ans)

	questions_ra = Question.objects.filter(is_solved=0).order_by('-created_date')
	answer_ra = []
	users_ra=[]
	for ques in questions_ra:
		user=Profile.objects.filter(user=ques.author)
		users_ra.append(user)
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_ra.append(ans)

	questions_na = Question.objects.filter(numAns=0).order_by('-created_date')
	answer_na = []
	users_na=[]
	for ques in questions_na:
		user=Profile.objects.filter(user=ques.author)
		users_na.append(user)
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_na.append(ans)

	questions_rq5= questions_rq[:5]
	answer_rq5 = answer_rq[:5]
	users_rq5 =users_rq[:5]
	# for ques in questions_rq:
	# 	user=Profile.objects.filter(user=ques.author)
	# 	users_rq.append(user)
	# 	answers = Answer.objects.filter(question=ques)
	# 	for ans in answers:
	# 		answer_rq.append(ans)

	pro_all = Profile.objects.order_by('-points')[:5]
	cuser=[]
	profiles = Profile.objects.all()
	context ={
				'users' : pro_all,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'questions_rq' : questions_rq,
				'answers_rq' : answer_rq,
				'questions_rq5' : questions_rq5,
				'answers_rq5' : answer_rq5,
				'questions_ma' : questions_ma,
				'answers_ma' : answer_ma,
				'questions_ra' : questions_ra,
				'answers_ra' : answer_ra,
				'questions_na' : questions_na,
				'answers_na' : answer_na,
				'users_rq' : users_rq,
				'users_ra' : users_ra,
				'users_ma' : users_ma,
				'users_na' : users_na,
				'all_profile' : profiles
			}
	if(request.user.username):
		showuser = User.objects.get(id = request.user.id)
		showprofile= Profile.objects.get(user=showuser)
		context ={
			# 'cuser': cuser,
			'users' : pro_all,
			'showUser' : showprofile,
			'questions_all' : questions_all,
			'answers_all' : answer_all,
			'questions_rq' : questions_rq,
			'answers_rq' : answer_rq,
			'questions_rq5' : questions_rq5,
			'answers_rq5' : answer_rq5,
			'questions_ma' : questions_ma,
			'answers_ma' : answer_ma,
			'questions_ra' : questions_ra,
			'answers_ra' : answer_ra,
			'questions_na' : questions_na,
			'answers_na' : answer_na,
			'users_rq' : users_rq,
			'users_ra' : users_ra,
			'users_ma' : users_ma,
			'users_na' : users_na,
			'all_profile' : profiles
		}
	# print(context)
	return render(request,'index.html', context)

def base(request):
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	pro_all = Profile.objects.order_by('-points')[:5]
	cuser=[]
	for pro in pro_all:
		if pro.username == request.user.username:
			cuser.append(pro)

	context = {
		'cuser': cuser,
		'questions_all' : questions_all,
		'answers_all' : answer_all
	}
	# print(context)
	return render(request,'base.html', context)

def login_site(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			# print(username)
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
			profile=Profile.objects.create(
					user=user,
					firstName=firstName,
					lastName=lastName,
					username=username,
					regDate=timezone.now(),
				)
			return redirect('/index/')
	else:
		return render(request, 'register.html')

def ask_question(request):
	if request.user.is_authenticated():
		# print('Authenticated')
		questions_all = Question.objects.all()
		answer_all = []
		for ques in questions_all:
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_all.append(ans)

		if request.method == 'POST':
			pro_all = Profile.objects.order_by('-points')[:5]
			cuser= []
			for pro in pro_all:
				if pro.username == request.user.username:
					pro.numQues+=1
					break;
			pro.save()
			# print('POST request')
			author = request.user
			question_title = request.POST['question_title']
			question_text = request.POST['question_text']
			tags = request.POST['tags[]']
			tags = tags.split(',');
			# print(tags)
			ques = Question.objects.create(
					author=author,
					question_title=question_title,
					question_text=question_text,
				)
			for tag in tags:
				try:
					t = Tag.objects.get(name=tag)
					t.question = Question.objects.get(question=ques)
					t.save()
				except ObjectDoesNotExist:
					t = Tag.objects.create(name=tag,
						question=ques)
			ques.save()
			return redirect('/index/')
		else:
			pro_all = Profile.objects.order_by('-points')[:5]
			cuser=[]
			for pro in pro_all:
				if pro.username == request.user.username:
					cuser.append(pro)
			showuser = User.objects.get(id = request.user.id)
			showprofile = Profile.objects.get(user=showuser)
			questions_rq = Question.objects.order_by('-created_date')[:5]
			answer_rq = []
			users_rq=[]
			for ques in questions_rq:
				user=Profile.objects.filter(user=ques.author)
				users_rq.append(user)
				answers = Answer.objects.filter(question=ques)
				for ans in answers:
					answer_rq.append(ans)
			
			context = {
				'users' : pro_all,
				'cuser': cuser,
				'showUser' : showprofile,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'questions_rq5': questions_rq,
				'answer_rq5' : answer_rq,
				'users_rq5' : users_rq,
			}
			# print('GET request')
			return render(request, 'ask_question.html', context)
	else:
		# print('Not Authenticated')
		return redirect('/login/')

def question_detail(request, question_id):
	flag=0
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
				pro_all = Profile.objects.order_by('-points')[:5]
				for pro in pro_all:
					if pro.username == request.user.username:
						pro.numAns+=1
						pro.points+=2
						break;
				pro.save()
				question.save()
				ans.save()
			else:
				# for key in request.POST:
					# print(key)
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
		
		pro_all = Profile.objects.order_by('-points')[:5]
		cuser=[]
		for pro in pro_all:
			if pro.username == request.user.username:
				cuser.append(pro)
		ques = Question.objects.get(id=question_id)
		
		ques.numViews+=1
		pq=Profile.objects.get(user=ques.author)
		
		answers = Answer.objects.filter(question=ques).order_by('-avotes').order_by('-bestAnswer')
		pa = []
		for ans in answers:
			print(ans.bestAnswer)
			print(ans)
			pro=Profile.objects.get(user=ans.author)
			pa.append(pro)
		# print(pa)
		c =[]
		pc=[]
		for ans in answers:
			com=Comment.objects.filter(answer=ans)
			c.append(com)
		pc=Profile.objects.all()

		questions_rq = Question.objects.order_by('-created_date')[:5]
		answer_rq = []
		users_rq=[]
		for quest in questions_rq:
			user=Profile.objects.filter(user=quest.author)
			users_rq.append(user)
			answers2 = Answer.objects.filter(question=ques)
			for ans in answers2:
				answer_rq.append(ans)
		if(request.user.username):
			showuser = User.objects.get(id = request.user.id)
			showprofile= Profile.objects.get(user=showuser)
			for ans in answers:
				# print(ans)
				if(ans.author.username != request.user.username):
					existingVotes=Vote.objects.filter(answer=ans)
					# print(existingVotes)
					for vote in existingVotes:
						if vote.voter==request.user:
							flag=1
							break
					# print(flag)
					if flag!=1: 
						answer=ans
						voter=request.user
						votes=Vote.objects.create(
								answer=answer,
								voter=voter,
								isVoted=0,
							)
						votes.save()
					flag=0

			context = {
				'users' : pro_all,
				'showUser' : showprofile,
				'profile_q' : pq,
				'profile_a' : pa,
				'all_profile' : pc,
				'question' : ques,
				'answers' : answers,
				'user' : request.user,
				'comments' : c,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'currProfile' : currProfile,
				'questions_rq5': questions_rq,
				'answer_rq5' : answer_rq,
				'users_rq5' : users_rq,
			}
		else:
			context = {
				'users' : pro_all,
				'profile_q' : pq,
				'profile_a' : pa,
				'all_profile' : pc,
				'question' : ques,
				'answers' : answers,
				'user' : request.user,
				'comments' : c,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'questions_rq5': questions_rq,
				'answer_rq5' : answer_rq,
				'users_rq5' : users_rq,
			}

		ques.save()
		# print(context)
		return render(request, 'question_detail.html', context)




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
		facebook=request.POST['fb']
		twitter=request.POST['twit']
		linkedin=request.POST['link']
		github=request.POST['github']

		# print(request.POST)
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
				if request.FILES['myfile']:
					myfile = request.FILES['myfile']
					fs = FileSystemStorage()
					filename = fs.save(myfile.name, myfile)
					pro.profilePic=filename
				pro.facebook=facebook
				pro.github=github
				pro.twitter=twitter
				pro.linkedin=linkedin
				break
		# if flag !=1:
		# 	pro=Profile.objects.create(
		# 			user=user,
		# 			firstName=fname,
		# 			lastName=lname,
		# 			username=username,
		# 			country=country,
		# 			website=website,
		# 			aboutYourself=about,
		# 			phone=phone,
		# 			regDate=timezone.now(),
		# 			profilePic=proPic,
		# 			facebook=facebook,
		# 			github=github,
		# 			twitter=twitter,
		# 			linkedin=linkedin,
		# 		)
		pro.save()
		user.first_name=fname
		user.last_name=lname
		user.username=username
		user.save()
		return redirect('/edit/')
	else:
		questions_all = Question.objects.all()
		answer_all = []
		for ques in questions_all:
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_all.append(ans)
		pro_all = Profile.objects.order_by('-points')[:5]
		cuser= []
		questions_rq = Question.objects.order_by('-created_date')[:5]
		answer_rq = []
		users_rq=[]
		for ques in questions_rq:
			user=Profile.objects.filter(user=ques.author)
			users_rq.append(user)
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_rq.append(ans)
		if (request.user.username):
			pro=Profile.objects.get(user=request.user)
			showuser = User.objects.get(id=request.user.id)
			if Profile.objects.get(user=showuser):
				showprofile=Profile.objects.get(user=showuser)
				context = {
				'users' : pro_all,
				'u_profile': pro,
				'showUser':showprofile,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'cuser' : cuser,
				'questions_rq5': questions_rq,
				'answer_rq5' : answer_rq,
				'users_rq5' : users_rq,
				}
			else:
				context = {
				'users' : pro_all,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'cuser' : cuser,
				'questions_rq5': questions_rq,
				'answer_rq5' : answer_rq,
				'users_rq5' : users_rq,
				}
	return render(request, 'edit_profile.html', context)
	
def search(request):
	if request.method == 'POST':
		pro_all = Profile.objects.order_by('-points')[:5]
		cuser=[]
		for pro in pro_all:
			if pro.username == request.user.username:
				cuser.append(pro)
		questions_all = Question.objects.all()
		answer_all = []
		for ques in questions_all:
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_all.append(ans)
		t = request.POST['question_title']
		# querywords = s.split()	#Who is Foo-Bar
		s=set(stopwords.words('english'))
		result = filter(lambda w: not w in s,t.split())
		# for word in querywords:
		# 	if word.lower() not in stopwords:
		# 		result.append(word)
		# print(result)
		query_title = Q()
		query_text = Q()
		# query_tt = Q()
		for word in result:
			query_title = query_title | Q(question_title__contains=word)
			query_text = query_text | Q(question_text__contains=word)
			# query_tt = query_text | Q(question_text__contains=word) | Q(question_title__contains=word)
			questions_title = Question.objects.filter(query_title)
			questions_text = Question.objects.filter(query_text)
			# questions_tt = Question.objects.filter(query_tt)
			# questions.append(Question.objects.filter(
			# 		question__Question_title__contains=word
			# 	)
			# )
		questions_tt = list(set().union(questions_title,questions_text))
		pc=Profile.objects.all()
		# print(pc)
		questions_rq = Question.objects.order_by('-created_date')[:5]
		answer_rq = []
		users_rq=[]
		for ques in questions_rq:
			user=Profile.objects.filter(user=ques.author)
			users_rq.append(user)
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_rq.append(ans)
		if(request.user.username):
			showuser = User.objects.get(id = request.user.id)
			showprofile= Profile.objects.get(user=showuser)
			context = {
				's' : t,
				'questions_tt' : questions_tt,
				'users' : pro_all,
				'cuser': cuser,
				'showUser':showprofile,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'allprofile' : pc,
				'questions_rq5': questions_rq,
				'answer_rq5' : answer_rq,
				'users_rq5' : users_rq,
			}
		else:
			context = {
				's' : t,
				'questions_tt' : questions_tt,
				'users' : pro_all,
				'cuser': cuser,
				'questions_all' : questions_all,
				'allprofile' : pc,
				'answers_all' : answer_all,
				'questions_rq5': questions_rq,
				'answer_rq5' : answer_rq,
				'users_rq5' : users_rq,
			}
		return render(request, 'search.html', context)
	else:
		return HttpResponse('What?')
def viewprofile(request, user_id):
	pro_all = Profile.objects.order_by('-points')[:5]
	cuser=[]
	for pro in pro_all:
		if pro.username == request.user.username:
			cuser.append(pro)
	showuser = User.objects.get(id = user_id)
	# print(showuser)

	

	showprofile = Profile.objects.get(user=showuser)
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	u_questions_all = Question.objects.filter(author=showuser)
	pro=Profile.objects.all()
	u_answers_all = Answer.objects.filter(author=showuser)
	u_answers_all_q=[]
	for u in u_answers_all:
		ques=Question.objects.get(id=u.question.id)
		u_answers_all_q.append(ques)
	u_answers_all_q=set(u_answers_all_q)
	u_comments_all = Comment.objects.filter(author=showuser)
	u_comments_all_a = []
	u_comments_all_q =[]
	for u in u_comments_all:
		ques=Question.objects.get(id=u.question.id)
		u_comments_all_q.append(ques)
		ans=Answer.objects.get(id=u.answer.id)
		u_comments_all_a.append(ans)
	u_comments_all_q=set(u_comments_all_q)
	u_comments_all_a=set(u_comments_all_a)
	questions_rq = Question.objects.order_by('-created_date')[:5]
	answer_rq = []
	users_rq=[]
	for ques in questions_rq:
		user=Profile.objects.filter(user=ques.author)
		users_rq.append(user)
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_rq.append(ans)

	if(request.user.username):
		currentUserProfile=Profile.objects.get(user=request.user)
		context = {
			'users': pro_all,
			'showuser' : showprofile,
			'showUser' : currentUserProfile,
			'u_questions_all' : u_questions_all,
			'u_answers_all' : u_answers_all,
			'u_answers_all_q' : u_answers_all_q,
			'u_comments_all' : u_comments_all,
			'u_comments_all_q' : u_comments_all_q,
			'u_comments_all_a' : u_comments_all_a,
			'questions_all' : questions_all,
			'answers_all' : answer_all,
			'allprofile': pro,
			'questions_rq5': questions_rq,
			'answer_rq5' : answer_rq,
			'users_rq5' : users_rq,
		}
	else: 
		context = {
			'users': pro_all,
			'showuser' : showprofile,
			'u_questions_all' : u_questions_all,
			'u_answers_all' : u_answers_all,
			'u_answers_all_q' : u_answers_all_q,
			'u_comments_all' : u_comments_all,
			'u_comments_all_q' : u_comments_all_q,
			'u_comments_all_a' : u_comments_all_a,
			'questions_all' : questions_all,
			'answers_all' : answer_all,
			'allprofile': pro,
			'questions_rq5': questions_rq,
			'answer_rq5' : answer_rq,
			'users_rq5' : users_rq,
		}
	# print(context)

	return render(request, 'viewprofile.html', context)


def countUp(request, answer_id):
	if request.user.is_authenticated():
		ans = Answer.objects.get(id=answer_id)
		voted=Vote.objects.filter(answer=ans).get(voter=request.user)
		if voted.isVoted==0:		
			ans.avotes+=1
			voted.isVoted=1
		elif voted.isVoted==1:
			ans.avotes-=1
			voted.isVoted=0
		elif voted.isVoted== -1:
			ans.avotes+=2
			voted.isVoted=1
		# print('isVoted='+ str(voted.isVoted))
		voted.save()
		# print(ans.avotes)
		pro_all = Profile.objects.all()
		for pro in pro_all:
			if(ans.author.username == pro.username):
				pro.points+=2
				pro.save()
		ans.save()
		return JsonResponse({
			"success": "true",
			"votes":ans.avotes
		})
	else:
		context={}
		context['error'] = 'You need to log in first.'
		return render(request,'login.html',context)

def countDown(request, answer_id):
	if request.user.is_authenticated():
		ans = Answer.objects.get(id=answer_id)
		voted=Vote.objects.filter(answer=ans).get(voter=request.user)
		if voted.isVoted==0:		
			ans.avotes-=1
			voted.isVoted=-1
		elif voted.isVoted==1:
			ans.avotes-=2
			voted.isVoted=-1
		elif voted.isVoted== -1:
			ans.avotes+=1
			voted.isVoted=0
		# print('isVoted='+ str(voted.isVoted))
		voted.save()
		pro_all = Profile.objects.all()
		for pro in pro_all:
			if(ans.author.username == pro.username):
				pro.points-=2
				pro.save()
		ans.save()
		return JsonResponse({
			"success": "true",
			"votes":ans.avotes
		})
	else:
		context={}
		context['error'] = 'You need to log in first.'
		return render(request,'login.html',context)

def bestanswer(request, answer_id):
	a = json.dumps(request.body.decode('utf-8'))
	# print (a)
	a = a.split('&csrfmiddlewaretoken')[0]
	question_id = a.split('ques_id=')[1]	
	q = Question.objects.get(id=question_id)
	q.is_solved = 1
	ans = Answer.objects.get(id=answer_id)
	ans.bestAnswer = 1
	ans.save()
	pro_all = Profile.objects.all()
	for pro in pro_all:
		if(ans.author.username == pro.username):
			pro.points+=10
			pro.save()
	q.save()
	return JsonResponse({
		"success" : "true",
		"status" : q.is_solved
		})

def reply_ajax(request, question_id):
	if request.user.is_authenticated():
		a = json.dumps(request.body.decode('utf-8'))
		# print (a)
		a = a.split('&csrfmiddlewaretoken')[0]
		a = a.split('value=')[1]
		text = a.split('&')[0]
		words = text.split('+')
		text = " ".join(words)
		text = urllib.unquote(text).decode('utf8')
		a_id = a.split('&')[1].split('=')[1]

		author=request.user
		answer=Answer.objects.get(id=a_id)
		ctext=text
		question=Question.objects.get(id=question_id)
		com = Comment.objects.create(
				author=author,
				comment_text=ctext,
				answer=answer,
				question=question
			)
		com.save()
		profile=Profile.objects.get(user=request.user)
		pic=profile.profilePic
		return JsonResponse({
			"success":"true",
			"text":text,
			"a_id":a_id,
			"name":request.user.username,
			"created_date":com.created_date,
			"pic":pic.path
			})
	else:
		context={}
		context['error'] = 'You need to log in first.'
		return render(request,'login.html',context)