# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from querysets import RestaurantQuerySet


class Borough(models.Model):
    name = models.CharField(max_length=255)


class Restaurant(models.Model):
    objects = RestaurantQuerySet.as_manager()

    name = models.CharField(max_length=255)
    borough = models.ForeignKey(Borough)
