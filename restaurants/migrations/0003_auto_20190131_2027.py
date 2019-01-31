# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-31 20:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_restaurant_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='grade',
            field=models.CharField(default='C', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='cuisine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.Cuisine'),
        ),
    ]