from scripts.formulas import HaversineDistance as haversine
from scripts.graphs import Graph
import heapq

class PriorityQueue():
    def __init__(self):
        self.__elements: List[Tuple[float, T]] = []

    def __str__(self):
        return str(self.__elements)

    def IsEmpty(self) -> bool:
        return not self.__elements

    def Insert(self, item, priority: float):
        heapq.heappush(self.__elements, (priority, item))

    def GetElement(self):
        return heapq.heappop(self.__elements)[1]

def Astar(graph: Graph, start, goal, balance:float=0.5, h_cost=haversine):
    """A* search to find the shortest path in adj from start to goal"""
    if not 0 <= balance <= 1: raise ValueError("Balance must be between 0 and 1")
    opened = PriorityQueue()
    opened.Insert(start, 0)
    
    camefrom = {}
    cost = {}

    camefrom[start] = None
    cost[start] = 0

    while not opened.IsEmpty():
        current = opened.GetElement()

        if current == goal: return PathFrom(goal, camefrom)

        for next in graph.GetNeighbors(current):
            newcost = cost[current] + graph.CostBetween(current, next, balance)
            if next not in cost or newcost < cost[next]:
                cost[next] = newcost
                f_cost = newcost + h_cost(next, goal)
                opened.Insert(next, f_cost)
                camefrom[next] = current

    return None

def PathFrom(goal, camefrom):
    path = []

    next = camefrom[goal]
    while not next == None:
        path.append(next)
        next = camefrom[next]

    path.reverse()
    path.append(goal)
    return path