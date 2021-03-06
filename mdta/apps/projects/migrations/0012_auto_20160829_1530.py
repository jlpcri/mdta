# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-29 20:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_auto_20160826_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='test_header',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_header', to='projects.Module'),
        ),
        migrations.AlterField(
            model_name='module',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]
