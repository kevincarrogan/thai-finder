# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.views.generic import View

from models import Cuisine, Restaurant


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

        top_10_restaurants = Restaurant.objects.all()

        cuisine_query = request.GET.get('cuisine')
        if cuisine_query:
            cuisine_to_filter_by = Cuisine.objects.get(name=cuisine_query)
            top_10_restaurants = top_10_restaurants.filter(cuisine=cuisine_to_filter_by)

        grade_query = request.GET.get('grade')
        if grade_query:
            top_10_restaurants = top_10_restaurants.filter(grade=grade_query)

        top_10_restaurants = top_10_restaurants.order_by('-score')[:10]

        for restaurant in top_10_restaurants:
            results.append({
                'name': restaurant.name,
                'score': restaurant.score,
            })

        return JsonResponse({
            'results': results,
        })
