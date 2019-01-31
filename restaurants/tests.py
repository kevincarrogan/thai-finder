# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.urlresolvers import reverse
from django.test import TestCase


class RestaurantTestCase(TestCase):

    def test_random_restaurant_endpoint_returns_ok_status_code(self):
        url = reverse('restaurants:random')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_random_restaurant_endpoint_returns_json_response(self):
        url = reverse('restaurants:random')

        response = self.client.get(url)
        json_response = json.loads(response.content)

        self.assertEqual(
            json_response,
            {
                'name': 'AROY DEE THAI KITCHEN',
                'borough': 'BRONX',
            },
        )
