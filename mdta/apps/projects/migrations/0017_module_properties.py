# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-08-07 20:49
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_project_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='properties',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]