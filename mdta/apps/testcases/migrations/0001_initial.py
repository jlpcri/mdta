# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-27 16:35
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.contrib.postgres.operations import HStoreExtension
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_auto_20160727_1131'),
    ]

    operations = [
        HStoreExtension(),

        migrations.CreateModel(
            name='TestCaseHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('results', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.hstore.HStoreField(), blank=True, null=True, size=None)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]