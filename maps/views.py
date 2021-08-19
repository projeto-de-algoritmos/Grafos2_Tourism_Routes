from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from maps.models import TouristAttraction
from maps.utils import center_geolocation


def map_view(request):
    attractions = TouristAttraction.objects.all()
    coords = []
    for attraction in attractions:
        coords.append(
            [float(attraction.latitude), float(attraction.longitude)]
        )

    median_lat, median_lng = center_geolocation(coords)
    mapbox_api_key = settings.MAPBOX_API_KEY

    return render(
        request,
        'map.html',
        {'attractions': attractions, 'median_lat': median_lat, 'median_lng': median_lng, 'api_key': mapbox_api_key}
    )
