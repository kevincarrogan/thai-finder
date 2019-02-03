# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from querysets import RestaurantQuerySet


class Borough(models.Model):
    name = models.CharField(max_length=255)


class Cuisine(models.Model):
    name = models.CharField(max_length=255)


class Restaurant(models.Model):
    objects = RestaurantQuerySet.as_manager()

    name = models.CharField(max_length=255)
    borough = models.ForeignKey(Borough)
    cuisine = models.ForeignKey(Cuisine, null=True)
    score = models.IntegerField(null=True)
    grade = models.CharField(null=True, max_length=1)
    rating_date = models.DateField(null=True)
    camis = models.IntegerField(unique=True)
