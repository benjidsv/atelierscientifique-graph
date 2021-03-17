from scripts.formulas import HaversineDistance as haversine
from scripts.pollutionmap import EstimatePathPollution as polcost
from scripts.graphdisplayer import PlotGraph
import matplotlib.pyplot as plt
import numpy as np

class Graph():
    def __init__(self, nodes:list, edges:list, polmap:dict=None, adj=None):
        self._nodes = nodes
        self._edges = edges
        self._polmap = polmap
        self._bbox = self.ComputePlotBBOX(nodes)
        self._adjacencylist = adj if adj else self.GenerateAdjacencyList(nodes, edges)

    def __str__(self):
        s = "====== NODE: NEIGHBORS ======\n"
        for node in self._adjacencylist:
            s += f"{node}: {self._adjacencylist[node]} \n"
        return s

    @classmethod
    def FromAdjacencyList(cls, adj:dict):
        """Creates a graph from an adjacency list instead of nodes and edges"""
        nodes = adj.keys()
        edges = []

        for node in nodes: # On parcourt chaque noeud
            for neighbor in adj[node]: # Puis ses voisins
                if [neighbor, node] not in edges: edges.append([node, neighbor]) # On ajoute la ligne si elle n'y est pas déjà

        return Graph(nodes, edges, adj)

    @classmethod
    def GenerateAdjacencyList(cls, nodes:list, edges:list) -> dict:
        """Returns the graph in the structure: dict{node: neighbors} to access it later"""
        adj = {}

        for node in nodes: adj[node] = []

        for edge in edges:
            adj[edge[0]].append(edge[1])
            adj[edge[1]].append(edge[0])
        
        return adj

    @classmethod
    def ComputePlotBBOX(cls, nodes:list) -> tuple:
        xmax, ymax, xmin, ymin = np.NINF, np.NINF, np.PINF, np.PINF
        for node in nodes:
            xmax, ymax = max(xmax, node[0]), max(ymax, node[1])
            xmin, ymin = min(xmin, node[0]), min(ymin, node[1])

        plt.scatter([xmax, xmin], [ymax, ymin])
        x, y = plt.xlim(), plt.ylim()
        plt.cla()

        return 0#x, y

    def ComputeNearestPoint(self, point:tuple, distance=haversine) -> tuple:
        shortest = np.PINF
        nearest = None

        for node in self._nodes:
            if node == point: return node
            d = distance(point, node)
            if d < shortest:
                shortest = d
                nearest = node
        return nearest

    def CostBetween(self, node1:tuple, node2:tuple, balance:float=0):
        if balance == 0 or not self._polmap: return haversine(node1, node2)
        return polcost(node1, node2, self._polmap) * balance + haversine(node1, node2) * (1 - balance)
        
    def GetNodes(self):
        return self._nodes

    def GetEdges(self):
        return self._edges

    def GetNeighbors(self, node):
        return self._adjacencylist.get(node, [])

    def GetPollutionMap(self):
        return self._polmap
    
    def GetBoundingBox(self):
        return self._bbox

    def GetAdjacencyList(self):
        return self._adjacencylist
        
    def SetPollutionMap(self, polmap:dict):
        self._polmap = polmap