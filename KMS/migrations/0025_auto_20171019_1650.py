# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-19 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KMS', '0024_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]