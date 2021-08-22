from collections import defaultdict
from math import sqrt

# Shortest path to all coordinates from any node
# Coordinates must be provided as a list containing lists of
# x/y pairs. ie [[23.2321, 58.3123], [x.xxx, y.yyy]]


def distance_between_coords(x1, y1, x2, y2):
    distance = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return distance


# Adds "names" to coordinates to use as keys for edge detection
def name_coords(coords):
    coord_count = 0
    for coord in coords:
        coord_count += 1
        coord.append(coord_count)
    return coords


# Creates a weighted and undirected graph
# Returns named coordinates and their connected edges as a dictonary
def build_graph(coords):
    coords = name_coords(coords)
    graph = defaultdict(list)
    edges = {}
    for current in coords:
        for comparer in coords:
            if comparer == current:
                continue
            else:
                weight = distance_between_coords(current[0], current[1],
                                                 comparer[0], comparer[1])
                graph[current[2]].append(comparer[2])
                edges[current[2], comparer[2]] = weight
    return coords, edges


# Returns a path to all nodes with least weight as a list of names
# from a specific node
def shortest_path(node_list, edges, start):
    neighbor = 0
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

def testando_shortest_path(graph_coords, graph_edges):
    shortest_path_taken = {}
    shortest_path_weight = 0
    all_paths = {}

    for index, node in enumerate(graph_coords):
        path, weight = shortest_path(graph_coords, graph_edges, index + 1)
        print('--------------------------------------')
        print("Path", index + 1, "=", path)
        print("Weight =", weight)
        all_paths[weight] = path
        if index == 0:
            shortest_path_weight = weight
            shortest_path_taken[weight] = path
        elif weight < shortest_path_weight:
            shortest_path_weight = weight
            shortest_path_taken[weight] = path
    print('--------------------------------------')
    print("The shortest path to all nodes is:", shortest_path_taken)
    print("The weight of the path is:", shortest_path_weight)
    return all_paths, shortest_path_taken

def convert_integer_to_string_path(attraction_names, paths):
    for weight, path in paths.items():
        converted_attractions = []
        for attraction_int in path:
            attraction_name_index = 0 if attraction_int == 1 else attraction_int - 1
            converted_attractions.append(attraction_names[attraction_name_index])
        paths[weight] = converted_attractions
