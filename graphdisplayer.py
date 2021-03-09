import numpy as np
import matplotlib.pyplot as plt
from hmconverter import GraphToEdgeList

def DEFAULT_CMAP():
    """Default pollution colormap. Returns a color depending on the pollution value"""

def PlotGraph(graph, path=None, polmap=None, cmap=DEFAULT_CMAP):
    """Plots a graph """
    #je pense que l'on mettra une valeur 1 pour moins de 10 une valeur 2 pour de 10 à 40 et 4 pour plus de 40
    edges = GraphToEdgeList(graph) # On récupère les cotés du graphe (les lignes qui le composent)
    for line in edges:
        plt.plot(*zip(*line), 'c') # On les affiche
    if path != None: plt.plot(*zip(*path), 'r') # Si un chemin est donné, on l'affiche
    if polmap: 
        for node in graph.keys(): 
            plt.scatter(node[0], node[1], c=polmap[node]) # Pareil pour la pollution
    plt.show()

"""
G = ox.graph_from_place('Massy, 91300, France', network_type='drive')
ox.plot_graph(G, bgcolor='black', show=True, save=True, filepath=imagepath)
plot = Image.open(imagepath)
width, height = plot.size
overlay = np.zeros([height, width, 4], dtype=np.uint8)
overlay[:,:] = [255, 0, 0, 255]
for x in range(height):
    for y in range(width):
        overlay[x, y, 3] = y
overlay = Image.fromarray(overlay)

overlay = MapToImage(1, (255, 0, 0, 255), plot.size)
image = Image.new("RGBA", (width, height))
image = Image.
alpha_composite(plot, overlay)
image.show()
"""