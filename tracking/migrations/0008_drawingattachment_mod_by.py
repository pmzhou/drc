# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-20 17:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracking', '0007_auto_20160120_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawingattachment',
            name='mod_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
