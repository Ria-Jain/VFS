# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
	author = models.ForeignKey(User)
	question_title = models.CharField(max_length=80)
	question_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	qvotes = models.IntegerField(default=0)
	numAns =models.IntegerField(default=0)
	numViews =models.IntegerField(default=0)
	# bestAnswer = models.ForeignKey(Answer)
	is_solved = models.IntegerField(default=0)
	recentAnswer=models.DateTimeField(auto_now_add=True)
	timeSince = models.CharField(max_length=1000, default='now')
	def __str__(self):
		return str(self.id) + " - " + self.author.username

class Tag(models.Model):
	name = models.CharField(max_length=1000, null=True)
	question = models.ForeignKey(Question)
	def __str__(self):
		return str(self.name) + " - " + str(self.question.id)


class Answer(models.Model):
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	bestAnswer = models.IntegerField(default=0)
	answer_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)
	dislikes=models.IntegerField(default=0)
	timeSince = models.CharField(max_length=1000, default='now')
	def __str__(self):
		return str(self.id) + " - " + self.author.username + " answered"
class Comment(models.Model):
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.ForeignKey(Answer)
	comment_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	timeSince = models.CharField(max_length=1000, default='now')
	def __str__(self):
		return self.author.username + " commented"

class Profile(models.Model):
	user= models.ForeignKey(User)
	firstName = models.CharField(max_length=100, default='')
	lastName = models.CharField(max_length=100, default='')
	username = models.CharField(max_length=100, default='')
	country = models.CharField(max_length=100, default='')
	website = models.CharField(max_length=100, default='')
	aboutYourself = models.CharField(max_length=500, default='')
	phone=models.CharField(max_length=10, default='')
	regDate=models.DateTimeField()
	profilePic=models.ImageField(upload_to='', default='avatar.png', max_length=1000)
	numAns=models.IntegerField(default=0)
	numQues=models.IntegerField(default=0)
	points=models.IntegerField(default=0)
	facebook=models.CharField(default='', max_length=100)
	github=models.CharField(default='', max_length=100)
	linkedin=models.CharField(default='', max_length=100)
	twitter=models.CharField(default='', max_length=100)
	def __str__(self):
		return str(self.id) + '-' + self.user.username + ' Profile'

class Vote(models.Model):
	voter = models.ForeignKey(User)
	answer = models.ForeignKey(Answer)
	like = models.IntegerField(default=0)
	dislike = models.IntegerField(default=0)
	def __str__(self):
		return str(self.voter.username) + " on " + str(self.answer.id)
