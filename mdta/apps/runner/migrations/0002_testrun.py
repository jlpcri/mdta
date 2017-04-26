# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-26 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20170404_1645'),
        ('runner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hat_run_id', models.IntegerField()),
                ('testrail_project_id', models.IntegerField()),
                ('testrail_suite_id', models.IntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
