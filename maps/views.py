from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages

from maps.models import TouristAttraction
from maps.utils import center_geolocation
from maps.graph_utils import build_graph, testando_shortest_path, convert_integer_to_string_path


def map_view(request):
    attractions = TouristAttraction.objects.filter(selected=True)
    coords = []
    if attractions:
        for attraction in attractions:
            print(float(attraction.latitude), float(attraction.longitude))
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
    else:
        messages.add_message(request, messages.ERROR, 'Selecione ao menos uma atração para exibí-la no mapa.')
        return redirect('/')


def list_attractions(request):
    attractions = TouristAttraction.objects.all().order_by('-selected')

    return render(
        request,
        'user_attractions.html',
        {'attractions': attractions}
    )

def remove_attraction(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.selected = False
    attraction.save()
    return redirect('/attractions')


def select_attraction(request, pk):
    attraction = TouristAttraction.objects.get(pk=pk)
    attraction.selected = True
    attraction.save()
    return redirect('/attractions')

def home(request):
    return render(
        request,
        'home.html'
    )

def test(request):
    attractions = TouristAttraction.objects.filter(selected=True)
    coords = []
    names = []
    if attractions:
        for attraction in attractions:
            coords.append(
                [float(attraction.latitude), float(attraction.longitude)]
            )
            names.append(attraction.name)

        median_lat, median_lng = center_geolocation(coords)
        mapbox_api_key = settings.MAPBOX_API_KEY

        graph_coords, graph_edges = build_graph(coords)
        all_paths, shortest_path = testando_shortest_path(graph_coords, graph_edges)

        geometries = []
        list_shortest_path = list(shortest_path.values())[0]

        #for index, attraction_identifier in enumerate(list_shortest_path[:-1]):
        #    current, next_ = attraction_identifier, list_shortest_path[index + 1]
        #    geometries.append((current, next_,))
        #    print(graph_edges[(current, next_,)])

        #convert_integer_to_string_path(names, all_paths)
        #shortest_path_weight = list(shortest_path.keys())[0]
        #shortest_path_converted = all_paths[shortest_path_weight]

        return render(
            request,
            'map.html',
            {'attractions': attractions, 'median_lat': median_lat, 'median_lng': median_lng, 'api_key': mapbox_api_key}
        )
    else:
        messages.add_message(request, messages.ERROR, 'Selecione ao menos uma atração para exibí-la no mapa.')
        return redirect('/')