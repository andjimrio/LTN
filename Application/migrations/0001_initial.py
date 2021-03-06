# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-28 15:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('pubDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('link_rss', models.URLField(max_length=500)),
                ('link_web', models.URLField(max_length=500)),
                ('description', models.TextField(blank=True)),
                ('language', models.CharField(blank=True, max_length=50)),
                ('logo', models.URLField(blank=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('link', models.URLField(max_length=500)),
                ('description', models.TextField()),
                ('image', models.URLField(max_length=500)),
                ('article', models.TextField()),
                ('pubDate', models.DateTimeField()),
                ('creator', models.CharField(max_length=500)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Application.Feed')),
            ],
            options={
                'ordering': ('-pubDate',),
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=250)),
                ('items', models.ManyToManyField(related_name='keywords', to='Application.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.BooleanField(default=False)),
                ('read', models.BooleanField(default=False)),
                ('web', models.BooleanField(default=False)),
                ('like', models.BooleanField(default=False)),
                ('saves', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='Application.Item')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(blank=True, max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='status',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='Application.UserProfile'),
        ),
        migrations.AddField(
            model_name='section',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='Application.UserProfile'),
        ),
        migrations.AddField(
            model_name='keyword',
            name='users',
            field=models.ManyToManyField(related_name='keywords', to='Application.UserProfile'),
        ),
        migrations.AddField(
            model_name='feed',
            name='sections',
            field=models.ManyToManyField(related_name='feeds', to='Application.Section'),
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Application.Item'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Application.UserProfile'),
        ),
    ]
