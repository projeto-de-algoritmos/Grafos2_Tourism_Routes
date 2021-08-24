from django.conf import settings

import requests


class MapboxClient(object):
    def __init__(self):
        self.host = 'https://api.mapbox.com'
        self.access_token = settings.MAPBOX_API_KEY

    def distance_between_coords(self, origin_coord, destination_coord):
        origin_lat, origin_lon = origin_coord
        destination_lat, destination_lon = destination_coord
        directions_endpoint = (
            f'{self.host}/directions/v5/mapbox/driving/{origin_lon}%2C{origin_lat}%3B{destination_lon}%2C{destination_lat}'
            f'?alternatives=false&geometries=geojson&steps=false&access_token={self.access_token}'
        )

        response = requests.get(directions_endpoint)
        response_json = response.json()
        distance = response_json['routes'][0]['distance']
        return distance
        
