# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.generic import View


class RandomRestaurantView(View):
    
    def get(self, *args, **kwargs):
        return HttpResponse('OK')
