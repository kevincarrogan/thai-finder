import csv
import datetime
import os

from django.core.management.base import BaseCommand
from django.db.utils import DataError

from restaurants.models import Borough, Cuisine, Restaurant


def extract_csv_data(csv_file):
    """Extracts csv data from a file skipping the first row
    """
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        yield row


def parse_csv_row(row):
    """Parses a row from the CSV and outputs a dictionary of this data.

    The data is cleaned making it acceptable to generate models in a later
    step.
    """
    try:
        score = int(row[13])
    except ValueError:
        score = None

    month, day, year = [int(x) for x in row[16].split('/')]
    rating_date = datetime.date(year, month, day)

    grade = row[14]
    if grade not in ['A', 'B', 'C', 'G', 'P', 'Z']:
        grade = None

    return {
        'camis': int(row[0]),
        'name': row[1].title(),
        'borough': row[2].title(),
        'cuisine': row[7].title(),
        'score': score,
        'grade': grade,
        'rating_date': rating_date,
    }


def create_models(data):
    """Creates models for Borough, Cuisine and Restaurant from already cleaned data.

    This function expects the data to have been validated, cleaned and normalised
    in a previous step.

    Will create the models handling any possible duplication.

    The grade for a restaurant will be updated if necessary.
    """
    borough, _ = Borough.objects.get_or_create(name=data['borough'])
    cuisine, _ = Cuisine.objects.get_or_create(name=data['cuisine'])

    model_data = data.copy()

    model_data.update({
        'borough': borough,
        'cuisine': cuisine,
    })
    camis = model_data.pop('camis')

    restaurant, created = Restaurant.objects.get_or_create(
        camis=camis,
        defaults=model_data,
    )

    if not created:
        grade = model_data['grade']
        rating_date = model_data['rating_date']
        if restaurant.rating_date is None or (rating_date and rating_date > restaurant.rating_date):
            restaurant.grade = grade
            restaurant.rating_date = rating_date
            restaurant.save()

    return restaurant, created


class Command(BaseCommand):
    help = 'Imports restaurant data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='The CSV file to import')

    def handle(self, *args, **options):
        file_path = os.path.join(os.getcwd(), options['filename'])
        saved_rows = 0
        created_restaurants = 0
        with open(file_path, 'r') as csv_file:
            for num_rows, row in enumerate(extract_csv_data(csv_file)):
                parsed_data = parse_csv_row(row)
                saved_rows = num_rows
                try:
                    _, created = create_models(parsed_data)
                except DataError:
                    self.stdout.write(
                        self.style.ERROR('Failed to import {}'.format(parsed_data)),
                    )
                if created:
                    created_restaurants += 1
        self.stdout.write(
            self.style.SUCCESS('Imported {} rows successfully.'.format(saved_rows + 1)),
        )
        self.stdout.write(
            self.style.SUCCESS('{} restaurants created.'.format(created_restaurants)),
        )
