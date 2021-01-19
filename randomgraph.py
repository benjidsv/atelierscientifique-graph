import random
from itertools import repeat

def GenerateRandomGraph(nodecount=0, startfinish=False):
    G = {}
    nodes = []

    if nodecount==0:
        nodecount = int(random.random() * random.randint(1, 1000))

    for i in repeat(None, nodecount):
        node = (int(random.random() * random.randint(-100, 100)), int(random.random() * random.randint(-100, 100)))
        nodes.append(node)

    for node in nodes:
        neighborcount = random.randint(1, int(nodecount / 5))
        neighbors = []
        for i in range(neighborcount):
            neighborindex = random.randint(0, len(nodes)-1)
            newneighbor = nodes[neighborindex]

            if newneighbor != node and newneighbor not in neighbors:
                neighbors.append(nodes[neighborindex])
        G[node] = neighbors

    if startfinish is True:
        start = nodes[random.randint(0, len(nodes)-1)]
        finish = nodes[random.randint(0, len(nodes)-1)]
        while finish == start:
            finish = nodes[random.randint(0, len(nodes)-1)]
        return G, start, finish

    return G  