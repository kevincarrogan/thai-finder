# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-03 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20190201_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='grade',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
