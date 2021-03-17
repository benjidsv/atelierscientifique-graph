import osmnx as ox
import os
from scripts.pollutionmap import GeneratePollutionMapRelativeToGraph
from scripts.hconverter import GetGraphFromData
from scripts.graphs import Graph
from scripts.bestpath import Astar
from scripts.graphdisplayer import PlotGraph
import matplotlib.pyplot as plt
import time

OG = {
        ( 0, 0) : [( 0, 1),( 1, 0),( 0,-1),( 0,-2)],
        ( 0, 1) : [( 0,-2),( 1, 1),( 0, 0)],
        ( 0,-1) : [( 0, 0),( 0,-2)],
        ( 0,-2) : [( 0, 1),( 0,-1),( 1,-2),(-1,-2),( 0, 0)],
        (-1, 0) : [(-1, 1),( 1, 0),( 0, 0)],
        (-1, 1) : [(-1, 0)],
        (-1,-2) : [( 0,-2)],
        ( 1, 0) : [( 1, 1),( 1,-2),(-1, 0),( 0, 0)],
        ( 1, 1) : [( 0, 1),( 1, 0)],
        ( 1,-2) : [( 1, 0),( 0,-2)],
    }
            #       -1  0     2 : x             #       -1  0     2 : x     
            #      1 o  o-----o                 #      1 0  0-----0
            #        |  |     |                 #        |  |     |
            #      0 o--o-----o                 #      0 0--0-----0
            #           |     |                 #           |     |
            #     -1    o     |                 #     -1   max    |
            #           |     |                 #           |     |
            #     -2 o--o-----o                 #     -2 0--0-----0
            #      :                            #      :
            #      y                            #      y

polmap = {
        ( 0, 0) : 0,
        ( 0, 1) : 0,
        ( 0,-1) :650,
        ( 0,-2) : 0,
        (-1, 0) : 0,
        (-1, 1) : 0,
        (-1,-2) : 0,
        ( 1, 0) : 0,
        ( 1, 1) : 0,
        ( 1,-2) : 0,
}

dir = os.path.abspath(os.path.dirname(__file__))

#oxgraph = ox.graph_from_place('Massy, 91300, France', simplify=False, network_type=)
oxgraph = ox.load_graphml(dir + '/ressources/graph.xml')# ox.load_graphml('C:/Users/benja/Desktop/Python/atelierscientifique-graph-main/ressources/graph.xml')
#startpoint, goalpoint = ox.distance.get_nearest_node(oxgraph, (48.72994, 2.2883)), ox.distance.get_nearest_node(oxgraph, ( 48.73449, 2.29273))
#start, goal = (oxgraph.nodes[startpoint]['x'], oxgraph.nodes[startpoint]['y']), (oxgraph.nodes[goalpoint]['x'],oxgraph.nodes[goalpoint]['y'])
#polmap = GeneratePollutionMapRelativeToGraph(oxgraph, dir + "/ressources/data10.csv")
graph = GetGraphFromData(oxgraph, polmap, 'graph')
print(graph)
#path = Astar(graph, start, goal, 0)
# plot only maxes: 0.051199665069580076 <= best
# plot nodes: 0.07337969064712524
PlotGraph(graph)