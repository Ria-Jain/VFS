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
import re
import operator
from django.db.models import Q
import json
import urllib
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from collections import Counter
from django.views.decorators.csrf import csrf_exempt



def timeSince(date):
	dt=timezone.now()-date
	offset=dt.seconds + (dt.days *24*60*60)
	
	delta_s = offset % 60
	delta_s = int(delta_s)

	offset /= 60
	delta_m = offset % 60
	delta_m =int(delta_m)
	
	offset /= 60
	delta_h = offset % 24
	delta_h = int(delta_h)
	
	offset /= 24
	delta_d = offset % 7 
	delta_d =int(delta_d)
	
	offset /= 7
	delta_w = offset 
	delta_w =int(delta_w)

	if delta_w > 1:
		st = str(delta_w) + ' weeks ago'
	elif delta_w == 1:
		st = '1 week ago'
	elif delta_d > 1:
		st = str(delta_d) + ' days ago'
	elif delta_d == 1:
		st = 'Yesterday'
	elif delta_h > 1:
		st = str(delta_h) + ' hours ago'
	elif delta_h == 1:
		st = 'An hour ago'
	elif delta_m > 1:
		st = str(delta_m) + ' minutes ago'
	elif delta_m == 1:
		st = 'A minute ago'
	elif delta_s >= 5:
		st = str(delta_s) + ' seconds ago'
	else: 
		st = 'now'

	return st


def index(request):
	tags_all = Tag.objects.all()
	tags = []
	for tag in tags_all:
		tags.append(tag.name)
	tagset = set(tags)
	ttttt = [[x,tags.count(x)] for x in set(tags)]
	toptags = []
	tagsnew = sorted(ttttt, key=operator.itemgetter(1), reverse=True)
	for i in tagsnew:
		# # print(i)
		toptags.append(i[0])
	toptags = toptags[:15]
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	profiles = Profile.objects.all()
	topThree = Profile.objects.order_by('-points')[:5]


	questions_rq5 = Question.objects.order_by('-created_date')[:5]

	questions_rq = Question.objects.order_by('-created_date')
	answer_rq = []
	for ques in questions_rq:
		date=ques.created_date
		ques.timeSince = timeSince(date)
		ques.save()
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_rq.append(ans)

	questions_ma = Question.objects.order_by('-numAns')
	answer_ma = []
	for ques in questions_ma:
		date=ques.created_date
		ques.timeSince = timeSince(date)
		ques.save()
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_ma.append(ans)

	questions_ra = Question.objects.filter(is_solved=0).order_by('-created_date')
	answer_ra = []
	for ques in questions_ra:
		date=ques.created_date
		ques.timeSince = timeSince(date)
		ques.save()
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_ra.append(ans)

	questions_na = Question.objects.filter(numAns=0).order_by('-created_date')
	answer_na = []
	for ques in questions_na:
		date=ques.created_date
		ques.timeSince = timeSince(date)
		ques.save()
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_na.append(ans)



	context ={
				'users' : topThree,
				'tags' : toptags,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'questions_rq' : questions_rq,
				'answers_rq' : answer_rq,
				'questions_rq5' : questions_rq5,
				'questions_ma' : questions_ma,
				'answers_ma' : answer_ma,
				'questions_ra' : questions_ra,
				'answers_ra' : answer_ra,
				'questions_na' : questions_na,
				'answers_na' : answer_na,
				'all_profile' : profiles
			}
	if(request.user.username):
		showprofile= Profile.objects.get(user=request.user)
		context['showUser']=showprofile

	return render(request,'index.html', context)

def login_site(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			pre = (request.META.get('HTTP_REFERER','/'))
			print(pre)
			pre = pre.split('/')
			prev = pre[-2]
			if prev == "login":
				return redirect('/index/')
			else:
				return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			context = {}
			context['error'] = "Wrong Credentials"
			return render(request, 'login.html',context)
	else:
		if request.user.is_authenticated():
			return redirect
		context = {}
		context['error'] = ''
		return render(request,'login.html', context)


def logout_site(request):
	logout(request)
	pre = (request.META.get('HTTP_REFERER','/'))
	pre = pre.split('/')
	prev = pre[-2]
	if prev == "logout":
		return redirect('/index/')
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	

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
		tags_all = Tag.objects.all()
		tags = []
		for tag in tags_all:
			tags.append(tag.name)
		tagset = set(tags)
		ttttt = [[x,tags.count(x)] for x in set(tags)]
		toptags = []
		tagsnew = sorted(ttttt, key=operator.itemgetter(1), reverse=True)
		for i in tagsnew:
			# # print(i)
			toptags.append(i[0])
		toptags = toptags[:15]
		questions_all = Question.objects.all()
		answer_all = []
		for ques in questions_all:
			answers = Answer.objects.filter(question=ques)
			for ans in answers:
				answer_all.append(ans)

		profiles = Profile.objects.all()
		topThree = Profile.objects.order_by('-points')[:5]


		questions_rq5 = Question.objects.order_by('-created_date')[:5]

		if request.method == 'POST':
			for pro in profiles:
				if pro.username == request.user.username:
					pro.numQues+=1
					break;
			pro.save()
			author = request.user
			question_title = request.POST['question_title']
			question_text = request.POST['question_text']
			tags = request.POST['tags[]']
			tags = tags.split(',');
			ques = Question.objects.create(
					author=author,
					question_title=question_title,
					question_text=question_text,
				)
			for tag in tags:
				t = Tag.objects.create(name=tag,
						question=ques)
			ques.save()
			return redirect('/index/')
		else:
			showprofile = Profile.objects.get(user=request.user)
			
			context = {
				'users' : topThree,
				'tagset' : tagset,
				'tags' : toptags,
				'showUser' : showprofile,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'questions_rq5': questions_rq5,
			}
			return render(request, 'ask_question.html', context)
	else:
		return redirect('/login/')

def question_detail(request, question_id):
	flag=0
	tags_all = Tag.objects.all()
	tags = []
	for tag in tags_all:
		tags.append(tag.name)
	tagset = set(tags)
	ttttt = [[x,tags.count(x)] for x in set(tags)]
	toptags = []
	tagsnew = sorted(ttttt, key=operator.itemgetter(1), reverse=True)
	for i in tagsnew:
		# # print(i)
		toptags.append(i[0])
	toptags = toptags[:15]

	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	profiles = Profile.objects.all()
	topThree = Profile.objects.order_by('-points')[:5]


	questions_rq5 = Question.objects.order_by('-created_date')[:5]
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
				for pro in profiles:
					if pro.username == request.user.username:
						pro.numAns+=1
						pro.points+=2
						break;
				pro.save()
				question.save()
				ans.save()
			else:
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
		ques.numViews+=1
		date=ques.created_date
		ques.timeSince = timeSince(date)
		ques.save()
		author=ques.author
		showuser=Profile.objects.get(user=author)
		ctags = []
		tags_all = Tag.objects.all()
		for tag in tags_all:
			if tag.question.id == ques.id:
				ctags.append(tag)
		l=len(ctags)
		related = []
		for i in range(0,l):
			related.append([])
		i=0
		for tag in ctags:
			for allt in tags_all:
				if tag.name == allt.name:
					if tag.question != allt.question:
						related[i].append(allt.question.id)
			i += 1
		
		close_q = Counter(x for sublist in related for x in sublist)
		related = []
		for i in close_q:
			q = Question.objects.get(id=i)
			related.append(q)
			related = related[0:5]
		
		answers = Answer.objects.filter(question=ques).order_by('-bestAnswer','-avotes')
		c=[]
		for ans in answers:
			com=Comment.objects.filter(answer=ans)
			c.append(com)
			for coms in com:
				date=coms.created_date
				coms.timeSince = timeSince(date)
				coms.save()
			
			date=ans.created_date
			ans.timeSince = timeSince(date)
			ans.save()

		context = {
			'related':related,
			'users' : topThree,
			'all_profile' : profiles,
			'question' : ques,
			'answers' : answers,
			'tags' : toptags,
			'comments' : c,
			'questions_all' : questions_all,
			'answers_all' : answer_all,
			'questions_rq5': questions_rq5,
			'showuser': showuser,
		}
		if(request.user.username):
			showprofile= Profile.objects.get(user=request.user)
			for ans in answers:
				if(ans.author.username != request.user.username):
					existingVotes=Vote.objects.filter(answer=ans)
					for vote in existingVotes:
						if vote.voter==request.user:
							flag=1
							break
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
			context['showUser']=showprofile
		return render(request, 'question_detail.html', context)




def edit(request):
	tags_all = Tag.objects.all()
	tags = []
	for tag in tags_all:
		tags.append(tag.name)
	tagset = set(tags)
	ttttt = [[x,tags.count(x)] for x in set(tags)]
	toptags = []
	tagsnew = sorted(ttttt, key=operator.itemgetter(1), reverse=True)
	for i in tagsnew:
		# print(i)
		toptags.append(i[0])
	toptags = toptags[:15]

	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	profiles = Profile.objects.all()
	topThree = Profile.objects.order_by('-points')[:5]


	questions_rq5 = Question.objects.order_by('-created_date')[:5]

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

		for pro in profiles:
			if pro.username == username:
				flag=1
				pro.firstName=fname
				pro.lastName=lname
				pro.country=country
				pro.website=website
				pro.aboutYourself=about
				pro.phone=phone
				if request.FILES:
					myfile = request.FILES['myfile']
					fs = FileSystemStorage()
					filename = fs.save(myfile.name, myfile)
					pro.profilePic=filename
				pro.facebook=facebook
				pro.github=github
				pro.twitter=twitter
				pro.linkedin=linkedin
				break
		pro.save()
		user.first_name=fname
		user.last_name=lname
		user.username=username
		user.save()
		return redirect('/viewprofile/'+ str(request.user.id) + '/')
	else:
		context = {
				'users' : topThree,
				'u_profile': profiles,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'tags' : toptags,
				'questions_rq5': questions_rq5,
				}
		if (request.user.username):
			showprofile=Profile.objects.get(user=request.user)
			context['showUser']=showprofile

	return render(request, 'edit_profile.html', context)
	
def edit_question(request,question_id):
	tags_all = Tag.objects.all()
	tags = []
	for tag in tags_all:
		tags.append(tag.name)
	tagset = set(tags)
	ttttt = [[x,tags.count(x)] for x in set(tags)]
	toptags = []
	tagsnew = sorted(ttttt, key=operator.itemgetter(1), reverse=True)
	for i in tagsnew:
		# print(i)
		toptags.append(i[0])
	toptags = toptags[:15]

	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	profiles = Profile.objects.all()
	topThree = Profile.objects.order_by('-points')[:5]
	question=Question.objects.get(id=question_id)
	questions_rq5 = Question.objects.order_by('-created_date')[:5]
	if request.method == 'POST':
		title=request.POST['question_title']
		text=request.POST['question_text']
		
		ques=Question.objects.get(id=question_id)
		ques.question_title=title
		ques.question_text=text
		ques.save()
		return redirect('/question_detail/'+ str(ques.id) + '/')
	context = {
				'users' : topThree,
				'u_profile': profiles,
				'questions_all' : questions_all,
				'answers_all' : answer_all,
				'tags' : toptags,
				'questions_rq5': questions_rq5,
				'question':question,
				}
	if (request.user.username):
		showprofile=Profile.objects.get(user=request.user)
		context['showUser']=showprofile
	return render(request, 'edit_question.html',context)

def search(request):
	tags_all = Tag.objects.all()
	tags = []
	for tag in tags_all:
		tags.append(tag.name)
	tagset = set(tags)
	ttttt = [[x,tags.count(x)] for x in set(tags)]
	toptags = []
	tagsnew = sorted(ttttt, key=operator.itemgetter(1), reverse=True)
	for i in tagsnew:
		# print(i)
		toptags.append(i[0])
	toptags = toptags[:15]

	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	profiles = Profile.objects.all()
	topThree = Profile.objects.order_by('-points')[:5]


	questions_rq5 = Question.objects.order_by('-created_date')[:5]
	if request.method == 'POST':
		t = request.POST['question_title']
		x = t
		t = re.sub('[^a-zA-Z0-9-_*.]', ' ', t)
		s = set(stopwords.words('english'))
		result = filter(lambda w: not w in s,t.split())
		# print(result)
		query_title = Q()
		query_text = Q()
		tags_all = Tag.objects.all()
		questions_tags = []
		questions_title = []
		questions_text = []
		for word in result:
			query_title = query_title | Q(question_title__contains=word)
			query_text = query_text | Q(question_text__contains=word)
			questions_title = Question.objects.filter(query_title)
			questions_text = Question.objects.filter(query_text)
			for tag in tags_all:
				if tag.name in word:
					questions_tags.append(
							Question.objects.get(id=tag.question.id)
						)
		questions_tt = []
		if len(questions_title) != 0:
			for i in questions_title:
				questions_tt.append(i)
		if len(questions_tags) != 0:
			for i in questions_tags:
				if i not in questions_tt:
					questions_tt.append(i)
		if len(questions_text) != 0:
			for i in questions_text:
				if i not in questions_tt:
					questions_tt.append(i)
		context = {
			's' : t,
			'questions_tt' : questions_tt,
			'tags' : toptags,
			'users' : topThree,
			'questions_all' : questions_all,
			'allprofile' : profiles,
			'answers_all' : answer_all,
			'questions_rq5': questions_rq5,
		}
		if(request.user.username):
			showprofile= Profile.objects.get(user=request.user)
			context['showUser']=showprofile
		return render(request, 'search.html', context)
	else:
		return HttpResponse('What?')

def viewprofile(request, user_id):
	tags_all = Tag.objects.all()
	tags = []
	for tag in tags_all:
		tags.append(tag.name)
	tagset = set(tags)
	ttttt = [[x,tags.count(x)] for x in set(tags)]
	toptags = []
	tagsnew = sorted(ttttt, key=operator.itemgetter(1), reverse=True)
	for i in tagsnew:
		# print(i)
		toptags.append(i[0])
	toptags = toptags[:15]

	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	profiles = Profile.objects.all()
	topThree = Profile.objects.order_by('-points')[:5]


	questions_rq5 = Question.objects.order_by('-created_date')[:5]

	user = User.objects.get(id = user_id)
	userProfile = Profile.objects.get(user=user)

	u_questions_all = Question.objects.filter(author=user).order_by('-created_date')
	for u in u_questions_all:
		date=u.created_date
		u.timeSince = timeSince(date)
		u.save()

	u_answers_all = Answer.objects.filter(author=user).order_by('-created_date')
	u_answers_all_q=[]
	for u in u_answers_all:
		ques=Question.objects.get(id=u.question.id)
		u_answers_all_q.append(ques)
		date=ques.created_date
		ques.timeSince = timeSince(date)
		ques.save()

		date=u.created_date
		u.timeSince = timeSince(date)
		u.save()
	u_answers_all_q=set(u_answers_all_q)

	u_comments_all = Comment.objects.filter(author=user).order_by('-created_date')
	u_comments_all_a = []
	u_comments_all_q =[]
	for u in u_comments_all:
		date=u.created_date
		u.timeSince = timeSince(date)
		u.save()

		ques=Question.objects.get(id=u.question.id)
		u_comments_all_q.append(ques)
		date=ques.created_date
		ques.timeSince = timeSince(date)
		ques.save()

		ans=Answer.objects.get(id=u.answer.id)
		u_comments_all_a.append(ans)
		date=ans.created_date
		ans.timeSince = timeSince(date)
		ans.save()

	u_comments_all_q=set(u_comments_all_q)
	u_comments_all_a=set(u_comments_all_a)

	context = {
		'users': topThree,
		'showuser' : userProfile,
		'u_questions_all' : u_questions_all,
		'u_answers_all' : u_answers_all,
		'u_answers_all_q' : u_answers_all_q,
		'u_comments_all' : u_comments_all,
		'u_comments_all_q' : u_comments_all_q,
		'u_comments_all_a' : u_comments_all_a,
		'tags' : toptags,
		'questions_all' : questions_all,
		'answers_all' : answer_all,
		'allprofile': profiles,
		'questions_rq5': questions_rq5,
	}
	# print(context)
	if(request.user.username):
		showprofile=Profile.objects.get(user=request.user)
		context['showUser']=showprofile

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
		voted.save()
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

def tagged(request, name):
	questions_all = Question.objects.all()
	answer_all = []
	for ques in questions_all:
		answers = Answer.objects.filter(question=ques)
		for ans in answers:
			answer_all.append(ans)

	profiles = Profile.objects.all()
	topThree = Profile.objects.order_by('-points')[:5]


	questions_rq5 = Question.objects.order_by('-created_date')[:5]
	tags_all = Tag.objects.all()
	questions = []
	for tag in tags_all:
		if tag.name == name:
			questions.append(tag.question)
	# print(questions)

	tags_all = Tag.objects.all()
	tags = []
	for tag in tags_all:
		tags.append(tag.name)

	tagsnew = Counter(tags)
	toptag = []
	for i in tagsnew:
		toptag.append(i)
	toptags = toptag[:15]


	context = {
		'questions' : questions,
		'name' : name,
		'users' : topThree,
		'questions_all' : questions_all,
		'all_profile' : profiles,
		'answers_all' : answer_all,
		'questions_rq5': questions_rq5,
		'tags' : toptags
	}
	if(request.user.username):
		showprofile=Profile.objects.get(user=request.user)
		context['showUser']=showprofile
	return render(request, 'tagged.html', context)

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
	# # print (a)
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

@csrf_exempt
def reply_ajax(request, question_id):
	if request.user.is_authenticated():
		a = json.loads(request.body.decode('utf-8'))
		print(a)
		# a = a.split('value=')[1]
		# text = a.split('&')[0]
		# words = text.split('+')
		# text = " ".join(words)
		# text = urllib.unquote(text).decode('utf8')
		# a_id = int(a.split('&')[1].split('=')[1].replace('"',''))
		a_id = a['ans_id']
		text = a['value']
		print(a_id, text)
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

# @csrf_exempt
# def reply_ajax(request, question_id):
# 	if request.user.is_authenticated():
# 		a = json.dumps(request.body.decode('utf-8'))
# 		print(a)
# 		a = a.split('value=')[1]
# 		text = a.split('&')[0]
# 		words = text.split('+')
# 		text = " ".join(words)
# 		text = urllib.unquote(text).decode('utf8')
# 		a_id = int(a.split('&')[1].split('=')[1].replace('"',''))

# 		author=request.user
# 		answer=Answer.objects.get(id=a_id)
# 		ctext=text
# 		question=Question.objects.get(id=question_id)
# 		com = Comment.objects.create(
# 				author=author,
# 				comment_text=ctext,
# 				answer=answer,
# 				question=question
# 			)
# 		com.save()
# 		profile=Profile.objects.get(user=request.user)
# 		pic=profile.profilePic
# 		return JsonResponse({
# 			"success":"true",
# 			"text":text,
# 			"a_id":a_id,
# 			"name":request.user.username,
# 			"created_date":com.created_date,
# 			"pic":pic.path
# 			})
# 	else:
# 		context={}
# 		context['error'] = 'You need to log in first.'
# 		return render(request,'login.html',context)