# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-06 03:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runner', '0009_automatedtestcase_tr_test_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testservers',
            old_name='server_url',
            new_name='hollytrace_url',
        ),
    ]
