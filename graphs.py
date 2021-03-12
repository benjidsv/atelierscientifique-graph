from formulas import HaversineDistance as haversine
from pollutionmap import EstimatePathPollution as polcost
from graphdisplayer import PlotGraph

class Graph():
    def __init__(self, nodes:list, edges:list, polmap:dict=None, adj=None):
        self.__nodes = nodes
        self.__edges = edges
        self.__polmap = polmap
        if adj: self.__adjacencylist = adj
        else: self.__adjacencylist = self.GenerateAdjacencyList(nodes, edges)

    def __str__(self):
        s = "====== NODE: NEIGHBORS ======\n"
        for node in self.__adjacencylist:
            s += f"{node}: {self.__adjacencylist[node]} \n"
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
    def GenerateAdjacencyList(self, nodes:list, edges:list) -> dict:
        """Returns the graph in the structure: dict{node: neighbors} to access it later"""
        adj = {}

        for node in nodes: adj[node] = []

        for edge in edges:
            adj[edge[0]].append(edge[1])
            adj[edge[1]].append(edge[0])
        
        return adj

    def CostBetween(self, node1:tuple, node2:tuple, balance:float=0):
        if balance == 0 or not self.__polmap: return haversine(node1, node2)
        return polcost(node1, node2, self.__polmap) * balance + haversine(node1, node2) * (1 - balance)
        
    def GetNodes(self):
        return self.__nodes

    def GetEdges(self):
        return self.__edges

    def GetNeighbors(self, node):
        return self.__adjacencylist.get(node, [])

    def GetPollutionMap(self):
        return self.__polmap

    def GetAdjacencyList(self):
        return self.__adjacencylist
        
    def SetPollutionMap(self, polmap:dict):
        self.__polmap = polmap