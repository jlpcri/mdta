# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-07 16:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edge',
            name='module',
        ),
    ]