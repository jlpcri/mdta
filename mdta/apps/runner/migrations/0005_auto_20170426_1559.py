# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-26 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0004_auto_20170426_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='automatedtestcase',
            name='call_id',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='automatedtestcase',
            name='failure_reason',
            field=models.TextField(default=''),
        ),
    ]
