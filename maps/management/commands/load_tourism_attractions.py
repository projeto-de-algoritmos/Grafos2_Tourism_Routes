import re

import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from maps.models import TouristAttraction


class Command(BaseCommand):
    help = 'Build graph from wikipedia page links using Kevin Bacon as starting node'

    def add_arguments(self, parser):
        parser.add_argument("--qty-cities", type=int,
                            help="number of cities to be searched within a page")

    def handle(self, *args, **kwargs):
        qty_attractions = kwargs["qty_attractions"] if "qty_attractions" in kwargs else 100
        csv_filename = 'new_york_attractions.csv'

        df_attractions = pd.read_csv(csv_filename, nrows=qty_attractions)

        # Create latitude and longitude from the_geom column in dataset
        df_attractions[['LNG', 'LAT']] = df_attractions['the_geom'].str.extract(r'POINT\s\((-\d{2}\.\d*)\s(\d{2}\.\d*)')

        model_instances = [
            TouristAttraction(
                name=attraction.NAME.capitalize(),
                city='New York',
                latitude=attraction.LAT,
                longitude=attraction.LNG
            )
            for attraction in df_attractions.itertuples()
        ]
        TouristAttraction.objects.bulk_create(model_instances)