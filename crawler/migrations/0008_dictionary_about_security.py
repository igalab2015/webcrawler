# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-07 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0007_auto_20160105_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary_about_security',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=63, verbose_name='word')),
            ],
        ),
    ]
