# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-24 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0003_auto_20170524_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='save',
        ),
        migrations.AddField(
            model_name='status',
            name='saves',
            field=models.BooleanField(default=False),
        ),
    ]
