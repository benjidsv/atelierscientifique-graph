from formulas import haversineDistance
from collections import deque

def BestPath(graph, start, goal, polmap, polscale=0.5, cost=haversineDistance, heuristic=haversineDistance):
    """Returns the path that is the best compromise between speed and pollution, according to the scale factor"""
    # Cet algo est une version modifiée de l'aglo BFS (une manière de parcourir un graphe)
    explored = []  # On stocke les noeuds déjà parcouru pour gagner du temps
    queue = [[start]] # Variable utilisée pour parcourir le graphe
      
    # Sécurité au cas ou le noeud de départ et d'arrivée sont identiques, on retourne un chemin nul
    if start == goal: 
        return None
      
    # On parcourt le graphe
    while queue: 
        path = queue.pop(0) 
        node = path[-1]
          
        # On passe uniquement sur les noeuds qu'on a pas déjà traités
        if node not in explored: 
            neighbours = graph[node] 
              
            # On regarde les voisins du noeud
            for neighbour in neighbours: 
                new_path = list(path) 
                new_path.append(neighbour) 
                queue.append(new_path) # On ajoute les voisins à la queue pour les parcourir au prochaine tour de boucle
                  
                # Si on est arrivé à la fin du graphe, on a trouvé le chemin
                if neighbour == goal: 
                    return new_path