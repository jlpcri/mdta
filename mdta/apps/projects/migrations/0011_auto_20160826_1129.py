# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-26 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20160817_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='version',
            field=models.TextField(default='version1'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='testrail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.TestRailConfiguration'),
        ),
    ]