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

start = choice(list(G.keys()))
finish = choice(list(G.keys()))
while start == finish:
        finish = choice(list(G.keys()))
path, cost = astar(G, start, finish) # TODO: trouver pk ça marche pas

DrawGraph(G, 0)
