# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-16 18:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0004_auto_20181214_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfav',
            name='goods',
            field=models.ForeignKey(help_text='商品的ID号', on_delete=django.db.models.deletion.CASCADE, related_name='fav_goods', to='goods.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='userfav',
            name='user',
            field=models.ForeignKey(help_text='用户的ID号', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='userleavingmessage',
            name='user',
            field=models.ForeignKey(help_text='用户的ID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
