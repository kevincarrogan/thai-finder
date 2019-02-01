import csv
import os

from django.core.management.base import BaseCommand

from restaurants.models import Borough, Cuisine, Restaurant


def extract_csv_data(csv_file):
    reader = csv.reader(csv_file)
    reader.next()
    for row in reader:
        yield row


def parse_csv_row(row):
    try:
        score = int(row[13])
    except ValueError:
        score = None

    return {
        'name': row[1].title(),
        'borough': row[2].title(),
        'cuisine': row[7].title(),
        'score': score,
        'grade': row[14],
    }


def create_models(data):
    borough, _ = Borough.objects.get_or_create(name=data['borough'])
    cuisine, _ = Cuisine.objects.get_or_create(name=data['cuisine'])

    data.update({
        'borough': borough,
        'cuisine': cuisine,
    })

    return Restaurant.objects.create(**data)


class Command(BaseCommand):
    help = 'Imports restaurant data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filename', help='The CSV file to import')

    def handle(self, *args, **options):
        file_path = os.path.join(os.getcwd(), options['filename'])
        saved_rows = 0
        with open(file_path, 'r') as csv_file:
            for num_rows, row in enumerate(extract_csv_data(csv_file)):
                parsed_data = parse_csv_row(row)
                saved_rows = num_rows
                create_models(parsed_data)
        self.stdout.write(
            self.style.SUCCESS('Imported {} rows successfully'.format(saved_rows + 1)),
        )
