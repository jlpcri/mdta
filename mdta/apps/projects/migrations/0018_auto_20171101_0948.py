# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-01 14:48
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_module_properties'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDatabaseSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(default='', help_text='A Memorable Word or Phrase', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='language',
            field=models.ForeignKey(blank=True, help_text='Selected Language under test', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_language', to='projects.Language'),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, help_text='People work on current project', related_name='project_members', to='users.HumanResource'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default='', help_text='A Memorable Word or Phrase', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='test_header',
            field=models.ForeignKey(blank=True, help_text='Part of Test Environment', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_header', to='projects.Module'),
        ),
        migrations.AlterField(
            model_name='project',
            name='testrail',
            field=models.ForeignKey(blank=True, help_text='Configuration connects to TestRail', null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.TestRailConfiguration'),
        ),
        migrations.AlterField(
            model_name='project',
            name='version',
            field=models.TextField(help_text='Sections of TestRail-Project'),
        ),
        migrations.AddField(
            model_name='projectdatabaseset',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='projectdatabaseset',
            unique_together=set([('project', 'name')]),
        ),
    ]
