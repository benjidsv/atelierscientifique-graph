import osmnx as ox
from pollutionmap import GeneratePollutionMapRelativeToGraph
from hmconverter import GetGraphFromData
from bestpath import BestPath
from graphdisplayer import PlotGraph

OG = {
        ( 0, 0) : [( 0, 1),( 2, 0),( 0,-1),( 0,-2)],
        ( 0, 1) : [( 0,-2),( 2, 1),( 0, 0)],
        ( 0,-1) : [( 0, 0),( 0,-2)],
        ( 0,-2) : [( 0, 1),( 0,-1),( 2,-2),(-1,-2),( 0, 0)],
        (-1, 0) : [(-1, 1),( 2, 0),( 0, 0)],
        (-1, 1) : [(-1, 0)],
        (-1,-2) : [( 0,-2)],
        ( 2, 0) : [( 2, 1),( 2,-2),(-1, 0),( 0, 0)],
        ( 2, 1) : [( 0, 1),( 2, 0)],
        ( 2,-2) : [( 2, 0),( 0,-2)],
    }
            #       -1  0     2 : x             #       -1  0     2 : x     
            #      1 o  o-----o                 #      1 0  0-----0
            #        |  |     |                 #        |  |     |
            #      0 o--o-----o                 #      0 0--0-----0
            #           |     |                 #           |     |
            #     -1    |     |                 #     -1    25    |
            #           |     |                 #           |     |
            #     -2 o--o-----o                 #     -2 0--0-----0
            #      :                            #      :
            #      y                            #      y

polmap = {
        ( 0, 0) : 0,
        ( 0, 1) : 0,
        ( 0,-1) :50,
        ( 0,-2) : 0,
        (-1, 0) : 0,
        (-1, 1) : 0,
        (-1,-2) : 0,
        ( 2, 0) : 0,
        ( 2, 1) : 0,
        ( 2,-2) : 0,
}

path, _ = BestPath(OG, (-1, 1), (-1,-2), polmap)
PlotGraph(OG, path, polmap)


G = ox.load_graphml('C:/Users/benja/Desktop/Python/atelierscientifique-graph-main/ressources/graph.xml')
polmap = GeneratePollutionMapRelativeToGraph(G, "C:/Users/benja/Desktop/Python/atelierscientifique-graph-main/ressources/data10.csv")
graph = GetGraphFromData(G, 'graph')

path, _ = BestPath(graph, list(graph.keys())[0], list(graph.keys())[500], polmap)
PlotGraph(graph, path, polmap)