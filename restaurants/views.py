# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.generic import View


class RandomRestaurantView(View):
    
    def get(self, *args, **kwargs):
        return JsonResponse({
            'name': 'AROY DEE THAI KITCHEN',
            'borough': 'BRONX',
        })
