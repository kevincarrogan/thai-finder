# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.generic import View

from models import Restaurant


class RandomRestaurantView(View):
    
    def get(self, request):
        try:
            restaurant = Restaurant.objects.random()
        except Restaurant.DoesNotExist:
            return JsonResponse({})

        return JsonResponse({
            'name': restaurant.name,
            'borough': restaurant.borough.name,
        })


class Top10RestaurantView(View):

    def get(self, request):
        results = []

        top_10_restaurants = Restaurant.objects.order_by('-score')[:10]

        for restaurant in top_10_restaurants:
            results.append({
                'name': restaurant.name,
                'score': restaurant.score,
            })

        return JsonResponse({
            'results': results,
        })
