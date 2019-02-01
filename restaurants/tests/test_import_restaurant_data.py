# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv

from StringIO import StringIO

from django.test import TestCase

from restaurants.management.commands.importrestaurantdata import (
    extract_csv_data,
    parse_csv_row,
    create_models,
)
from restaurants.models import Borough, Cuisine, Restaurant


class ImportRestaurantDataTestCase(TestCase):

    def _generate_csv_file_in_memory(self, rows):
        in_memory_file = StringIO()
        csv.writer(in_memory_file).writerows(rows)
        in_memory_file.seek(0)
        return in_memory_file

    def test_extract_csv_data(self):
        csv = self._generate_csv_file_in_memory([['ignored'], ['realdata']])
        extracted = list(extract_csv_data(csv))
        self.assertEqual(extracted, [['realdata']])

    def test_parse_csv_row(self):
        row = ['50054551', 'BURGER KING/POPEYES', 'BRONX', '217', 'E FORDHAM RD', '10458', '3473446815', 'Hamburgers', '10/17/2016', 'Violations were cited in the following area(s).', '08A', 'Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist.', 'Not Critical', '12', 'A', '10/17/2016', '01/30/2019', 'Pre-permit (Operational) / Initial Inspection']
        parsed_row = parse_csv_row(row)
        self.assertEqual(
            parsed_row,
            {
                'grade': 'A',
                'cuisine': 'Hamburgers',
                'borough': 'Bronx',
                'name': 'Burger King/Popeyes',
                'score': 12,
            }
        )

    def test_create_models(self):
        self.assertEqual(Borough.objects.count(), 0)
        self.assertEqual(Cuisine.objects.count(), 0)
        self.assertEqual(Restaurant.objects.count(), 0)

        row = {
            'grade': 'A',
            'cuisine': 'Hamburgers',
            'borough': 'Bronx',
            'name': 'Burger King/Popeyes',
            'score': 12,
        }
        restaurant = create_models(row)

        self.assertEqual(Borough.objects.count(), 1)
        self.assertEqual(Cuisine.objects.count(), 1)
        self.assertEqual(Restaurant.objects.count(), 1)

        borough = Borough.objects.get()
        self.assertEqual(borough.name, 'Bronx')

        cuisine = Cuisine.objects.get()
        self.assertEqual(cuisine.name, 'Hamburgers')

        self.assertEqual(restaurant.name, 'Burger King/Popeyes')
        self.assertEqual(restaurant.grade, 'A')
        self.assertEqual(restaurant.score, 12)
        self.assertEqual(restaurant.borough, borough)
        self.assertEqual(restaurant.cuisine, cuisine)

    def test_create_models_uses_existing_related_models(self):
        borough = Borough.objects.create(name='Bronx')
        cuisine = Cuisine.objects.create(name='Hamburgers')

        row = {
            'grade': 'A',
            'cuisine': 'Hamburgers',
            'borough': 'Bronx',
            'name': 'Burger King/Popeyes',
            'score': 12,
        }
        restaurant = create_models(row)

        self.assertEqual(Borough.objects.count(), 1)
        self.assertEqual(Cuisine.objects.count(), 1)
        self.assertEqual(Restaurant.objects.count(), 1)

        self.assertEqual(restaurant.name, 'Burger King/Popeyes')
        self.assertEqual(restaurant.grade, 'A')
        self.assertEqual(restaurant.score, 12)
        self.assertEqual(restaurant.borough, borough)
        self.assertEqual(restaurant.cuisine, cuisine)
