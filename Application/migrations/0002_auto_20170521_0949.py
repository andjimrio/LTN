# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-21 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='language',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='feed',
            name='link_rss',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='feed',
            name='link_web',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='feed',
            name='logo',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='item',
            name='link',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='section',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.URLField(blank=True, max_length=500),
        ),
    ]