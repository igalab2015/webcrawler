# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url_list',
            name='title',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='タイトル'),
        ),
    ]
