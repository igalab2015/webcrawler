# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0005_auto_20151226_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crawled_url_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=255, unique=True, verbose_name='URL')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Title')),
            ],
        ),
    ]
