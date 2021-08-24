from collections import defaultdict
from math import sqrt
from maps.client import MapboxClient


def build_graph(coords):
    graph = defaultdict(list)
    edges = {}
    mapbox_client = MapboxClient()
    for current in coords:
        for comparer in coords:
            if comparer == current:
                continue
            else:
                weight = mapbox_client.distance_between_coords(
                    [current[0], current[1]],
                    [comparer[0], comparer[1]]
                )
                graph[current[2]].append(comparer[2])
                edges[current[2], comparer[2]] = weight
    return coords, edges


def shortest_path(node_list, edges, start):
    unvisited = []
    visited = []
    total_weight = 0
    current_node = start

    for node in node_list:
        node_identifier = node[2]
        if node_identifier == start:
            visited.append(start)
        else:
            unvisited.append(node_identifier)
    while unvisited:
        for index, neighbor in enumerate(unvisited):
            if index == 0:
                current_weight = edges[start, neighbor]
                current_node = neighbor
            elif edges[start, neighbor] < current_weight:
                current_weight = edges[start, neighbor]
                current_node = neighbor
        total_weight += current_weight
        unvisited.remove(current_node)
        visited.append(current_node)
    return visited, total_weight

def dijkstra(graph_coords, graph_edges):
    shortest_path_taken = {}
    shortest_path_weight = 0
    all_paths = {}
    graph_coords_without_first_position = graph_coords[1:]

    for index, node in enumerate(graph_coords_without_first_position):
        attraction_name = node[2]
        path, weight = shortest_path(graph_coords, graph_edges, attraction_name)
        all_paths[weight] = path
        if index == 0:
            shortest_path_weight = weight
            shortest_path_taken[weight] = path
        elif weight < shortest_path_weight:
            if list(shortest_path_taken.keys()):
                previous_shortest_path_taken = list(shortest_path_taken.keys())[0]
                del shortest_path_taken[previous_shortest_path_taken]
            shortest_path_weight = weight
            shortest_path_taken[weight] = path
    return all_paths, shortest_path_taken
