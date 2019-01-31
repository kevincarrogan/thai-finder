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

    NUMBER_OF_RESULTS = 10

    def _get_query_set(self):
        return Restaurant.objects.all()

    def _filter_query_set_from_request(self, query_set, request):
        foreign_key_filter_keys = [
            ('cuisine', Cuisine),
        ]
        for key, related_model_class in foreign_key_filter_keys:
            query_value = request.GET.get(key)
            if query_value:
                try:
                    object_to_filter_by = related_model_class.objects.get(name=query_value)
                except related_model_class.DoesNotExist:
                    # If we can't find a lookup for our object we can just
                    # quickly return no results instead of trying more filters
                    return self._get_query_set().none()
                else:
                    query_set = query_set.filter(**{key: object_to_filter_by})

        filter_keys = ['grade']
        for key in filter_keys:
            query_value = request.GET.get(key)
            if query_value:
                query_set = query_set.filter(**{key: query_value})

        return query_set

    def _limit_query_set(self, query_set):
        return query_set.order_by('-score')[:self.NUMBER_OF_RESULTS]

    def _get_results(self, query_set):
        results = []

        for restaurant in query_set:
            results.append({
                'name': restaurant.name,
                'score': restaurant.score,
            })

        return results

    def get(self, request):
        query_set = self._get_query_set()
        filtered_query_set = self._filter_query_set_from_request(query_set, request)
        limited_query_set = self._limit_query_set(filtered_query_set)

        return JsonResponse({
            'results': self._get_results(limited_query_set),
        })
