import numpy as np
import matplotlib.pyplot as plt
from hmconverter import GraphToEdgeList

def ColorMap(polmap):
    """Default pollution colormap. Returns a color depending on the pollution value"""
    colors = []
    for node in polmap: # On regarde chaque valeur de pollution
        colors.append((0, 0.4, 0, Normalize(polmap[node]))) # Et on assigne une transparence (alpha) en fonction de la valeur
    print(colors)
    return colors

def Normalize(value, rmin=0, rmax=650, tmin=0, tmax=1):
    """Normalizes value between tmin and tmax"""
    return (value - rmin)/(rmax - rmin) * (tmax - tmin) + tmin

def PlotGraph(graph, path=None, polmap=None):
    """Plots a graph """
    edges = GraphToEdgeList(graph) # On récupère les cotés du graphe (les lignes qui le composent)
    for line in edges:
        plt.plot(*zip(*line), 'c') # On les affiche

    if path: 
        if polmap: plt.scatter(*zip(*path), c='b', zorder=4) # On redessine les points si une polmap est fournie, sinon on a des trous
        plt.plot(*zip(*path), 'b', zorder=2) # Si un chemin est donné, on l'affiche

    if polmap: plt.scatter(*zip(*polmap), c=ColorMap(polmap), zorder=3) # Pareil pour la pollution
    
    plt.show() # Le paramètre zorder permet de s'assurer de l'ordre dans le lequel les dessins sont affichés

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
