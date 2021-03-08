import osmnx as ox
import time
from debug import printMsg

def getGraphFromData(data, mode='path', showMessage = False):
    printMsg("=================== START FILE CONVERSION ===================", showMessage)
    startTime = time.time()
    graph = createGraph(data)
    printMsg(("Took : " + str(time.time() - startTime) + " seconds to make a graph from the file."), showMessage)
    printMsg("=============================================================", showMessage)
    return graph
  
def createGraph(data, mode='path'):
    """Loads a OSMNX xml graph and converts it"""
    graph = {}
    
    if mode == 'path': oxgraph = ox.load_graphml(data)
    if mode == 'query': oxgraph = ox.graph_from_place(data, network_type='drive')
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
