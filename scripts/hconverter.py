import osmnx as ox
from scripts.graphs import Graph

kwargs = {
            'network_type':"all_private",
            'simplify':True,
            'retain_all':False,
            'truncate_by_edge':False,
            'which_result':None,
            'buffer_dist':None,
            'clean_periphery':True,
            'custom_filter':None,
        }

def GetGraphFromData(data, polmap:dict=None, mode='path', querydelimiter='|'):
    """Loads a OSMNX xml graph and converts it to a Graph"""
    if mode == 'path': oxgraph = ox.load_graphml(data)
    elif mode == 'query': 
        query = data.split('|')
        userargs = dict(e.split('=') for e in query[1].split(','))
        for arg in userargs:
            kwargs[arg] = userargs[arg]
        kwargs['query'] = query[0]
        oxgraph = ox.graph_from_place(**kwargs)
    elif mode == 'graph': oxgraph = data
    else: 
        print('ValueError => Supported modes are: path, query, graph. Given mode: ' + mode)
        return None #raise ValueError("Supported modes are: path, query, graph")

    nodes = [(node[1]['x'], node[1]['y']) for node in oxgraph.nodes(data=True)]
    edges = [[(oxgraph.nodes[edge[0]]['x'], oxgraph.nodes[edge[0]]['y']), (oxgraph.nodes[edge[1]]['x'], oxgraph.nodes[edge[1]]['y'])] 
              for edge in oxgraph.edges]

    return Graph(nodes, edges, polmap)