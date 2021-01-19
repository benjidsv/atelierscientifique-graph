from graphdisplayer import DrawGraph
from dependencies.shortpath import astar
from converter import GetGraphFrom
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

G = GetGraphFrom(Path(__file__) / "../ressources/massy") # TODO: optimiser le code de converter (ça prend trop de temps)

#path, cost = astar(G, start, finish) ne marche pas avec shortpath (je crois que ça passe pas avec les float)

DrawGraph(G, 0)