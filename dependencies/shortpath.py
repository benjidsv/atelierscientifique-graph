import math
from dependencies.geometry import x, y, euclidian_distance


def astar(graph, start, goal, cost = euclidian_distance, heuristic = euclidian_distance):
    opened = set()
    closed = set()
    m_heur = {}
    m_parent = {}
    m_cost = {} # absolute path costs

    def path_from(node):
        def parents(node):
            while node:
                yield node
                node = m_parent.get(node, None)
        path  = [p for p in parents(node)]
        cost = m_cost[goal]
        path.reverse()
        return path,cost

    opened.add(start)
    m_cost[start] = 0
    while opened:
        # sort opened nodes based on the heuristic and consider the first one
        current = sorted(opened, key=lambda n : m_heur.get( n, heuristic(n,goal) ) )[0]
        if current == goal:
            # FIXME add backtrack validation
            return path_from(current)

        closed.add(current)
        opened.remove(current)

        for neighbor in graph[current]:
            if neighbor in closed:
                continue

            elif neighbor in opened:
                next_cost = m_cost[current] + cost(current,neighbor)
                if next_cost < m_cost[neighbor]:
                    m_cost[neighbor] = next_cost
                    m_parent[neighbor] = current
            else:
                m_cost[neighbor] = m_cost[current] + cost(current,neighbor)
                m_heur[neighbor] = heuristic( neighbor, goal )
                m_parent[neighbor] = current
                opened.add(neighbor)
    return []