import numpy as np
from scripts.formulas import HaversineDistance as haversine
from PIL import Image
import pandas as pd

AVERAGE_PM10 = 0 #150.0

def GeneratePollutionMap(csvpath, pollutionheader='PM10'):
    """Generates a pollution map from the data given (csv format)"""
    polmap = {}

    data = pd.read_csv(csvpath, sep=';', usecols=['latitude', 'longitude', pollutionheader])
    for i in range(data.shape[0]):
        polmap[data['latitude'][i], data['longitude'][i]] = data[pollutionheader][i]

    return polmap

def GeneratePollutionMapRelativeToGraph(graph, csvpath, pollutionheader='PM10'):
    """Generates and a pollution map from the data given (csv format) relative to a given graph."""
    polmap = {}
    
    data = pd.read_csv(csvpath, sep=';', usecols=['latitude', 'longitude', pollutionheader]) # On lit les données

    for i in range(data.shape[0]):
        nearestid = nearest(graph, (data['latitude'][i], data['longitude'][i])) 
        if (graph.nodes[nearestid]['x'], graph.nodes[nearestid]['y']) in polmap: # On regarde si une valeur existe déjà
            polmap[graph.nodes[nearestid]['x'], graph.nodes[nearestid]['y']] = (polmap[graph.nodes[nearestid]['x'],
             graph.nodes[nearestid]['y']] + data[pollutionheader][i])/2 # On calcule la moyenne si une il y a déjà une valeur
        else: polmap[graph.nodes[nearestid]['x'], graph.nodes[nearestid]['y']] = data[pollutionheader][i] # Sinon on l'ajoute

    return polmap

def ColorMap(polmap):
    """Default pollution colormap. Returns a color depending on the pollution value"""
    colors = []
    for node in polmap: # On regarde chaque valeur de pollution
        colors.append((0, 0.4, 0, Normalize(polmap[node]))) # Et on assigne une transparence (alpha) en fonction de la valeur
    return colors

def MapToImage(graph, color=(255, 0, 0, 255), size=(1860, 1012)):
    """Generates a png RGBA overlay with of pollution map, the higher the pollution the higher the opacity"""
    width, height = size
    overlay = np.zeros([height, width, 4], dtype=np.uint8)
    overlay[:,:] = [255, 0, 0, 255]
    overlay = Image.fromarray(overlay)
    return overlay

def EstimatePathPollution(node1:tuple, node2:tuple, polmap):
        return (polmap.get(node1, AVERAGE_PM10) + polmap.get(node2, AVERAGE_PM10))