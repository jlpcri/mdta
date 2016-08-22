# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-22 16:12
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20160817_1432'),
        ('testcases', '0002_auto_20160819_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCaseResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('results', django.contrib.postgres.fields.jsonb.JSONField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
