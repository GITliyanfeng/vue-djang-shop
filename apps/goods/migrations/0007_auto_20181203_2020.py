# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-03 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_auto_20181126_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategory',
            name='desc',
            field=models.TextField(default='', help_text='类别描述', max_length=200, verbose_name='类别描述'),
        ),
    ]
