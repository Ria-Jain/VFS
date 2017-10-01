# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from KMS.models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
# admin.site.register(isVoted)
admin.site.register(Profile)
