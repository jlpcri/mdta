# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-09 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20160830_1312'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='humanresource',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
    ]