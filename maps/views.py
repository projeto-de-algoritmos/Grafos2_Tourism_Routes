from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages
from django.utils.safestring import mark_safe

from maps.models import TouristAttraction
from maps.utils import center_geolocation
from maps.graph_utils import build_graph, calculate_shortest_path


def list_attractions(request):
    attractions = TouristAttraction.objects.all().order_by('-selected')
    if attractions:
        return render(
            request,
            'user_attractions.html',
            {'attractions': attractions}
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'É necessário existir atrações na base de dados para poder selecioná-las. '
            'Verifique se já foi feita a importação do arquivo de atrações turísticas para a base de dados.'
        )
        return redirect('/')

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

def map_view(request):
    attractions = TouristAttraction.objects.filter(selected=True)
    coords = []
    names = []
    if attractions and attractions.count() > 1:
        for attraction in attractions:
            coords.append(
                [float(attraction.latitude), float(attraction.longitude), attraction.name]
            )
            names.append(attraction.name)

        median_lat, median_lng = center_geolocation(coords)
        mapbox_api_key = settings.MAPBOX_API_KEY

        graph_coords, graph_edges = build_graph(coords)
        all_paths, shortest_path = calculate_shortest_path(graph_coords, graph_edges)

        geometries = []
        shortest_path_distance = list(shortest_path.keys())[0]
        shortest_path_attractions = list(shortest_path.values())[0]
        ordered_paths = []
        fastest_path_string = (
            f'O caminho mais rápido percorre uma distância aproximada de <strong>{round(shortest_path_distance/1000, 2)}</strong> quilômetros '
            f'ao percorrer as seguintes atrações: {shortest_path[shortest_path_distance][0]}'
        )
        for i, attraction_name in enumerate(shortest_path_attractions):
            if i:
                fastest_path_string += f', <strong>{attraction_name}</strong>'
            attraction = TouristAttraction.objects.filter(name=attraction_name).first()
            ordered_paths.append(
                {
                    'latitude': attraction.latitude,
                    'longitude': attraction.longitude,
                    'name': attraction.name,
                }
            )
        fastest_path_string
        return render(
            request,
            'map.html',
            {'attractions': ordered_paths, 'fastest_path_string': mark_safe(fastest_path_string),  'median_lat': median_lat, 'median_lng': median_lng, 'api_key': mapbox_api_key}
        )
    elif attractions.count() == 1:
        messages.add_message(
            request,
            messages.ERROR,
            'É necessário selecionar mais de uma atração para traçar o menor caminho entre elas.'
        )
        return redirect('/')
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'Selecione ao menos uma atração para verificar o menor caminho para visitar todas as atrações. '
        )
        return redirect('/')