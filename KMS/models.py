# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
	author = models.ForeignKey(User)
	topic = models.CharField(max_length=80)
	question_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.author.first_name
class Answer(models.Model):
	author = models.ForeignKey(User)
	question = models.ForeignKey(Question)
	answer_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.author.first_name + " answered"
class Comment(models.Model):
	author = models.ForeignKey(User)
	answer = models.ForeignKey(Answer)
	comment_text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.author.first_name + " commented"