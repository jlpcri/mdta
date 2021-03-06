# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-26 21:45
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.contrib.postgres.operations import HStoreExtension
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        HStoreExtension(),

        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='')),
                ('priority', models.SmallIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('property', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EdgeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True)),
                ('keys', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None, verbose_name='Keys(Separated with comma)')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('property', django.contrib.postgres.fields.hstore.HStoreField(blank=True, null=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Module')),
            ],
        ),
        migrations.CreateModel(
            name='NodeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, unique=True)),
                ('keys', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None, verbose_name='Keys(Separated with comma)')),
            ],
        ),
        migrations.AddField(
            model_name='node',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphs.NodeType'),
        ),
        migrations.AddField(
            model_name='edge',
            name='from_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_node', to='graphs.Node'),
        ),
        migrations.AddField(
            model_name='edge',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Module'),
        ),
        migrations.AddField(
            model_name='edge',
            name='to_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_node', to='graphs.Node'),
        ),
        migrations.AddField(
            model_name='edge',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphs.EdgeType'),
        ),
    ]
