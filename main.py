from graphdisplayer import DrawGraph
from dependencies.shortpath import astar
from converterV2 import *
from pathlib import Path
from random import choice

OG = {
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

G = getGraphFrom(Path(__file__) / "../ressources/massy") # TODO: optimiser le code de converter (ça prend trop de temps)

#start = (48.7190002, 2.2533135)
#finish = (48.7189578, 2.2533583)
#path, cost = astar(G, start, finish)

#DrawGraph(G, path)
