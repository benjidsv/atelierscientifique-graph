from pathlib import Path
from converterV2 import *
from graph_algorithms import *
from display import *
from debug import *

graphTest_1 = {
        ( 0, 0) : [( 0,-1),( 0, 1),( 2, 0),( 0,-2)],
        ( 0, 1) : [( 0,-2),( 2, 1),( 0, 0)],
        ( 0,-2) : [( 0, 1),( 2,-2),(-1,-2),( 0, 0)],
        (-1, 0) : [(-1, 1),( 2, 0),( 0, 0)],
        (-1, 1) : [(-1, 0)],
        (-1,-2) : [( 0,-2)],
        ( 2, 0) : [( 2, 1),( 2,-2),(-1, 0),( 0, 0)],
        ( 2, 1) : [( 0, 1),( 2, 0)],
        ( 2,-2) : [( 2, 0),( 0,-2)],
    }
            #       -1  0     2 : x
            #      1 o  o-----o
            #        |  |     |
            #      0 o--o-----o
            #           |     |
            #     -1    |     |
            #           |     |
            #     -2 o--o-----o
            #      :
            #      y

showMessage = True

"""Get graph from file if filepath isn't equals to None, else get a test graph"""
def getGraph(file = None) :
    if file :
        return getGraphFromFile(Path(__file__) / file, showMessage)
    return graphTest_1

"""Get path from graph with the specified function. Allow user to select best way or just a classic way"""
def getPathFromGraph(graph, start, end, shortest = True) :
    if shortest:
        return findShortestPath(graph, start, end)
    return findPath(graph, start, end)

"""Main, code executed in first"""
def main(start, end, file = None):
    graph = getGraph(file) # Get a graph
    #path = getPathFromGraph(graph, start, end) # Get a path
    #displayGraph(graph, path) # Display the graph to the user's screen

"""main(starting coordinates, ending coordinates, "File to load")"""
#main((48.7189581, 2.2533580), (48.7189578, 2.2533583), "../ressources/massy")
debugConverterPerformanceComparator(Path(__file__) / "../ressources/massy", 15, showMessage = True)
