import numpy as np
from osmnx.distance import get_nearest_node as nearest
from PIL import Image
import pandas as pd

""" La fonction a opti est GeneratePollutionMapRelativeToGraph:
    On prend un graphe osmnx (d'osm) et les données du pollubike, et vu que les points données par le pollubike correspondent pas au graphe,
    On prend pour chaque point pollubike le point le + proche dans le graphe, le problème c'est que ça veut dire qu'on doit parcourir le
    graphe en entier pour chaque point de pollubike (la fonction nearest parcourt tout le graphe pour trouver le point le + proche). Des idées
    pour améliorer ça ? Temps d'éxec sur mon pc: environ 15s"""

def GeneratePollutionMap(csvpath, pollutionheader='PM10'):
    """Generates a pollution map from the data given (csv format)"""
    map = {}

    data = pd.read_csv(csvpath, sep=';', usecols=['latitude', 'longitude', pollutionheader])
    for i in range(data.shape[0]):
        map[data['latitude'][i], data['longitude'][i]] = data[pollutionheader][i]

    return map

def GeneratePollutionMapRelativeToGraph(graph, csvpath, pollutionheader='PM10'):
    """Generates and a pollution map from the data given (csv format) relative to a given graph."""
    map = {}

    data = pd.read_csv(csvpath, sep=';', usecols=['latitude', 'longitude', pollutionheader])
    for i in range(data.shape[0]):
        nearestid = nearest(graph, (data['latitude'][i], data['longitude'][i])) 
        map[graph.nodes[nearestid]['x'], graph.nodes[nearestid]['y']] = data[pollutionheader][i]

    return map

def MapToImage(map, color=(255, 0, 0, 255), size=(1860, 1012)):
    """Generates a png RGBA overlay with of pollution map, the higher the pollution the higher the opacity"""
    width, height = size
    overlay = np.zeros([height, width, 4], dtype=np.uint8)
    overlay[:,:] = [255, 0, 0, 255]
    overlay = Image.fromarray(overlay)
    return overlay

if __name__ == '__main__':
    path = "C:/Users/benja/Desktop/Python/atelierscientifique-graph-main/ressources/data10.csv"
    map = GeneratePollutionMap(path)
    print(map)