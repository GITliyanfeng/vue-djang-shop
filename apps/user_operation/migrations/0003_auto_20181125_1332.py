# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-25 13:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0002_auto_20181125_1229'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userleavingmessage',
            old_name='msg_type',
            new_name='message_type',
        ),
    ]
