# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 16:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0005_auto_20160614_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edge',
            name='name',
        ),
    ]
