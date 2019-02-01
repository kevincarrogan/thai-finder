# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-01 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Borough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('score', models.IntegerField(null=True)),
                ('grade', models.CharField(max_length=1)),
                ('camis', models.IntegerField(unique=True)),
                ('borough', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.Borough')),
                ('cuisine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.Cuisine')),
            ],
        ),
    ]
