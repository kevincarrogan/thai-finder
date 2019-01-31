# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Borough, Cuisine, Restaurant


class RandomRestaurantTestCase(TestCase):

    def setUp(self):
        self.url = reverse('restaurants:random')

    def test_random_restaurant_endpoint_returns_ok_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_random_restaurant_endpoint_no_data_json_response(self):
        response = self.client.get(self.url)

        self.assertEqual(response.json(), {})

    def test_random_restaurant_endpoint_returns_json_response(self):
        borough = Borough.objects.create(name='BRONX')
        restaurant = Restaurant.objects.create(
            borough=borough,
            name='AROY DEE THAI KITCHEN',
            score=0,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.json(),
            {
                'name': 'AROY DEE THAI KITCHEN',
                'borough': 'BRONX',
            },
        )

    def test_random_restaurant_endpoint_returns_random_restaurant(self):
        borough = Borough.objects.create(name='BRONX')
        restaurant = Restaurant.objects.create(
            borough=borough,
            name='AROY DEE THAI KITCHEN',
            score=0,
        )
        other_restaurant = Restaurant.objects.create(
            borough=borough,
            name='Thai Cottage',
            score=0,
        )

        with patch('restaurants.views.Restaurant') as MockModel:
            MockModel.objects.random.return_value = restaurant
            response = self.client.get(self.url)
            self.assertEqual(
                response.json(),
                {
                    'name': 'AROY DEE THAI KITCHEN',
                    'borough': 'BRONX',
                },
            )

        with patch('restaurants.views.Restaurant') as MockModel:
            MockModel.objects.random.return_value = other_restaurant
            response = self.client.get(self.url)
            self.assertEqual(
                response.json(),
                {
                    'name': 'Thai Cottage',
                    'borough': 'BRONX',
                },
            )


class Top10RestaurantsTestCase(TestCase):

    def setUp(self):
        self.url = reverse('restaurants:top10')

    def test_top10_restaurant_endpoint_returns_ok_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_top10_restaurant_endpoint_no_data_json_response(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.json(),
            {
                'results': [],
            },
        )

    def test_top10_restaurants_returns_results(self):
        borough = Borough.objects.create(name='Bronx')
        for i in range(1, 21):
            Restaurant.objects.create(
                borough=borough,
                name='Restaurant with score of {}'.format(i),
                score=i,
            )

        response = self.client.get(self.url)
        self.assertEqual(
            response.json(),
            {
                'results': [
                    {'name': 'Restaurant with score of 20', 'score': 20},
                    {'name': 'Restaurant with score of 19', 'score': 19},
                    {'name': 'Restaurant with score of 18', 'score': 18},
                    {'name': 'Restaurant with score of 17', 'score': 17},
                    {'name': 'Restaurant with score of 16', 'score': 16},
                    {'name': 'Restaurant with score of 15', 'score': 15},
                    {'name': 'Restaurant with score of 14', 'score': 14},
                    {'name': 'Restaurant with score of 13', 'score': 13},
                    {'name': 'Restaurant with score of 12', 'score': 12},
                    {'name': 'Restaurant with score of 11', 'score': 11},
                ]
            },
        )

    def test_top10_restaurants_with_filters(self):
        borough = Borough.objects.create(name='Bronx')
        thai_cuisine = Cuisine.objects.create(name='Thai')
        thai_restaurant = Restaurant.objects.create(
            name='A Thai restaurant',
            grade='A',
            score=10,
            cuisine=thai_cuisine,
            borough=borough,
        )

        indian_cuisine = Cuisine.objects.create(name='Indian')
        indian_restaurant = Restaurant.objects.create(
            name='An Indian restaurant',
            grade='B',
            score=10,
            cuisine=indian_cuisine,
            borough=borough,
        )

        url = '{}?cuisine=Thai'.format(self.url)
        response = self.client.get(url)
        self.assertEqual(
            response.json(),
            {
                'results': [
                    {'name': 'A Thai restaurant', 'score': 10},
                ]
            },
        )

        url = '{}?cuisine=Indian'.format(self.url)
        response = self.client.get(url)
        self.assertEqual(
            response.json(),
            {
                'results': [
                    {'name': 'An Indian restaurant', 'score': 10},
                ]
            },
        )

        url = '{}?cuisine=Thai&grade=A'.format(self.url)
        response = self.client.get(url)
        self.assertEqual(
            response.json(),
            {
                'results': [
                    {'name': 'A Thai restaurant', 'score': 10},
                ]
            },
        )

    def test_top10_restaurants_unknown_foreign_key_filter_returns_no_results(self):
        borough = Borough.objects.create(name='Bronx')
        thai_cuisine = Cuisine.objects.create(name='Thai')
        thai_restaurant = Restaurant.objects.create(
            name='A Thai restaurant',
            grade='A',
            score=10,
            cuisine=thai_cuisine,
            borough=borough,
        )

        url = '{}?cuisine=madeup'.format(self.url)
        response = self.client.get(url)
        self.assertEqual(
            response.json(),
            {
                'results': [],
            },
        )

    def test_top10_restaurants_keys_are_case_insensitive(self):
        borough = Borough.objects.create(name='Bronx')
        thai_cuisine = Cuisine.objects.create(name='Thai')
        thai_restaurant = Restaurant.objects.create(
            name='A Thai restaurant',
            grade='A',
            score=10,
            cuisine=thai_cuisine,
            borough=borough,
        )

        url = '{}?cuisine=thai'.format(self.url)
        response = self.client.get(url)
        self.assertEqual(
            response.json(),
            {
                'results': [{'name': 'A Thai restaurant', 'score': 10}],
            },
        )

        url = '{}?cuisine=THAI'.format(self.url)
        response = self.client.get(url)
        self.assertEqual(
            response.json(),
            {
                'results': [{'name': 'A Thai restaurant', 'score': 10}],
            },
        )
