from math import radians, sin, cos, asin, sqrt

EARTH_RADIUS = 6371.0088 # km

def HaversineDistance(point1, point2):
    lat1, lon1, lat2, lon2 = map(radians, [point1[0], point1[1], point2[0], point2[1]])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) 
    return c * EARTH_RADIUS * 1000 # mètres

def  EuclidianDistance(point1, point2):
    x1, y1, x2, y2 = point1[0], point1[1], point2[0], point2[1]
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5