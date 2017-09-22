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
	recentAnswer=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.id) + " - " + self.author.username
class Answer(models.Model):
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	avotes = models.IntegerField(default=0)
	def __str__(self):
		return str(self.id) + " - " + self.author.username + " answered"
class Comment(models.Model):
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer = models.ForeignKey(Answer)
	comment_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.author.username + " commented"

class Profile(models.Model):
	user= models.ForeignKey(User)