# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-31 20:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
