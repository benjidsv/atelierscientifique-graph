import osmnx as ox
from graphs import Graph

def GetGraphFromData(data, polmap:dict=None, mode='path'):
    """Loads a OSMNX xml graph and converts it to a Graph"""
    if mode == 'path': oxgraph = ox.load_graphml(data)
    elif mode == 'query': oxgraph = ox.graph_from_place(data, network_type='drive')
    elif mode == 'graph': oxgraph = data
    else: raise ValueError("Supported modes are: path, query, graph")

    nodes = [(node[1]['x'], node[1]['y']) for node in oxgraph.nodes(data=True)]
    edges = [[(oxgraph.nodes[edge[0]]['x'], oxgraph.nodes[edge[0]]['y']), (oxgraph.nodes[edge[1]]['x'], oxgraph.nodes[edge[1]]['y'])] 
              for edge in oxgraph.edges]

    return Graph(nodes, edges, polmap)