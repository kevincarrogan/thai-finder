# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from models import Borough, Restaurant


class RandomRestaurantTestCase(TestCase):

    def setUp(self):
        self.url = reverse('restaurants:random')

    def test_random_restaurant_endpoint_returns_ok_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_random_restauran_endpoint_no_data_json_response(self):
        response = self.client.get(self.url)

        self.assertEqual(response.json(), {})

    def test_random_restaurant_endpoint_returns_json_response(self):
        borough = Borough.objects.create(name='BRONX')
        restaurant = Restaurant.objects.create(
            borough=borough,
            name='AROY DEE THAI KITCHEN',
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.json(),
            {
                'name': 'AROY DEE THAI KITCHEN',
                'borough': 'BRONX',
            },
        )
