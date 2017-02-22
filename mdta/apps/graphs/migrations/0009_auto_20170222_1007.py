# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-22 16:07
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0008_auto_20160830_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='verbiage',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='nodetype',
            name='verbiage_keys',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None, verbose_name='VerbiageKeys(Separated with comma)'),
        ),
    ]