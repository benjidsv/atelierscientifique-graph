# Allègrement ctrl+C - ctrl+V de : https://www.python.org/doc/essays/graphs/
def findPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not(start in graph):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = findPath(graph, node, end, path)
            if newpath: return newpath
    return None

def findShortestPath(graph, start, end, path = []): # Fonction récursive
    path = path + [start] # On ajoute au chemin courant passé en paramètre, le point de départ.
    
    if start == end : # Si on est arrivé, alors on renvoi le chemin
        return path

    if not(start in graph) : # Si le point de départ n'est pas dans le graph, on renvoie None
        return None

    shortestPath = None # Liste qui stockera le chemin le plus cours à partir de cette profondeur de récursivité
    for node in graph[start] : # Pour tous les voisins de notre cellule de départ à partir de cette profondeur de récursivité
        if node not in path : # On vérifie que nous ne somme pas déjà passé par là avec le chemin courant
            newPath = findShortestPath(graph, node, end, path) # On fait l'appel récursif (start doit-être remplacé parle voisin)
            if newPath != None and (not shortestPath or len(newPath) < len(shortestPath)): # Si la longueur du chemin récupéré lors de l'appel récursif est plus petite que la longueur du plus chemin à partir des voisin, alors il devient le plus court chemin
                shortestPath = newPath
    return shortestPath # Renvoi du chemin le plus court pour atteindre end à partir de start
