# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-17 15:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_auto_20181217_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordergoods',
            old_name='goods_num',
            new_name='nums',
        ),
    ]
