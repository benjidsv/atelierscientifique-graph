import osmnx as ox
from matplotlib.collections import LineCollection as LC

def GetGraphFromData(data, mode='path'):
    """Loads a OSMNX xml graph and converts it"""
    graph = {}
    
    if mode == 'path': oxgraph = ox.load_graphml(data)
    elif mode == 'query': oxgraph = ox.graph_from_place(data, network_type='drive')
    elif mode == 'graph': oxgraph = data
    else: raise ValueError("Mode not supported.")

    for nodeid in oxgraph:
        graph[oxgraph.nodes[nodeid]['x'], oxgraph.nodes[nodeid]['y']] = []

    for edge in oxgraph.edges:
        length = len(edge) - 1

        for i in range(length):
            e = graph.get((oxgraph.nodes[edge[i]]['x'], oxgraph.nodes[edge[i]]['y']), [])

            if length > 1 and i == 0:
                if edge[1] not in e:
                    graph[oxgraph.nodes[edge[i]]['x'], oxgraph.nodes[edge[i]]['y']].append((oxgraph.nodes[edge[1]]['x'],
                                                                                           oxgraph.nodes[edge[1]]['y']))
            elif i == (length - 1):
                if edge[length - 2] not in e:
                    graph[oxgraph.nodes[edge[i]]['x'], oxgraph.nodes[edge[i]]['y']].append((oxgraph.nodes[edge[i - 1]]['x'],
                                                                                           oxgraph.nodes[edge[i - 1]]['y']))
            else:
                if edge[i - 1] not in e:
                    graph[oxgraph.nodes[edge[i]]['x'], oxgraph.nodes[edge[i]]['y']].append((oxgraph.nodes[edge[i - 1]]['x'],
                                                                                           oxgraph.nodes[edge[i - 1]]['y']))
                if edge[i + 1] not in e:
                    graph[oxgraph.nodes[edge[i]]['x'], oxgraph.nodes[edge[i]]['y']].append((oxgraph.nodes[edge[i + 1]]['x'],
                                                                                           oxgraph.nodes[edge[i + 1]]['y']))
    return graph


def GraphToEdgeList(graph):
    """Converts a graph to an edge list, useful to plot it"""
    explored = [] # On stocke les noeuds déjà parcourus pour éviter les doublons
    edges = []

    for node in graph: # On parcourt chaque noeud
        for neighbor in graph[node]: # Puis ses voisins
            if neighbor in explored: continue
            edges.append([node, neighbor]) # On ajoute la ligne a notre liste
        explored.append(node) # On note le noeud comme parcouru
    
    return edges