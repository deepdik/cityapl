# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-25 21:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_message_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='messages_receiver', to=settings.AUTH_USER_MODEL, verbose_name='receiver'),
        ),
    ]
