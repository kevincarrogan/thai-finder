from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Imports restaurant data from a CSV file'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('OK'))
