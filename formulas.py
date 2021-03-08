from math import radians, sin, cos, asin, sqrt

EARTH_RADIUS = 6371.0088 # km

def haversineDistance(point1, point2):
    lat1, lon1, lat2, lon2 = map(radians, [point1[0], point1[1], point2[0], point2[1]])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) 
    return c * EARTH_RADIUS * 1000