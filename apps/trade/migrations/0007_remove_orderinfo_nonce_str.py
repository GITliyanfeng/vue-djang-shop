# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-17 15:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_auto_20181217_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinfo',
            name='nonce_str',
        ),
    ]
