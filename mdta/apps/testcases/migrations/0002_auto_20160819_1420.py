# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-19 19:20
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testcases', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcasehistory',
            name='name',
        ),
        migrations.AlterField(
            model_name='testcasehistory',
            name='results',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), blank=True, null=True, size=None),
        ),
    ]