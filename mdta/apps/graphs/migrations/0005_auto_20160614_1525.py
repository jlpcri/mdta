# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-14 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0004_auto_20160610_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edge',
            name='priority',
            field=models.SmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
    ]
