# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-30 11:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='seen',
        ),
    ]