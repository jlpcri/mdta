# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 17:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0002_auto_20160519_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='project',
        ),
        migrations.AlterField(
            model_name='edge',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Module'),
        ),
        migrations.AlterField(
            model_name='node',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Module'),
        ),
        migrations.DeleteModel(
            name='Module',
        ),
    ]
