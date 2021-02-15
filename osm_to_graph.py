#!/usr/bin/env python3

import xml.etree.ElementTree as et

def add_node(elem, graph, coordinates):
    """Add the given element's ID to the graph and its lon/lat to the coordinates."""
    node = int(elem.attrib.get("id"))
    graph[node] = graph.get(node,[])
    coordinates[node] = {
            "lon":float(elem.attrib.get("lon")),
            "lat":float(elem.attrib.get("lat"))
        }


def add_neighbors(elems, graph):
    """Add the given way (an ordered sequence of elements) to the graph."""
    if len(elems) < 2:
        return # O or 1 element: not a proper way.

    # Iterate over pairs.
    for i in range(len(elems)-1):
        node_A = int(elems[i  ].attrib.get("ref"))
        node_B = int(elems[i+1].attrib.get("ref"))
        # A is neighbor of B and …
        graph.get(node_A,[]).append(node_B)
        # … B is neighbor of A.
        graph.get(node_B,[]).append(node_A)


def parse(data):
    """Parse the given data stream and return the corresponding
    graph (a dictionary mapping unique node IDs to a list of neighbor nodes)
    and coordinates (a dictionary mapping IDs to lon/lat)."""
    coordinates = {}
    graph = {}

    # It's always better to let someone actually get the data
    # and just process the data in functions,
    # because there is many ways to get the data (open a file, a stream, etc.).
    etree = et.parse(data)

    # Loop only once over the XML tree.
    for elem in etree.iter():
        if elem.tag == "node":
            add_node(elem, graph, coordinates)

        elif elem.tag == "way":
            elems = elem.findall("nd")
            add_neighbors(elems, graph)

    return graph,coordinates


def clean(graph,coordinates):
    """Remove nodes which have no neighbor."""
    # TODO merge simple edges to get an even cleaner graph.
    clean_graph = {}
    clean_coordinates = {}
    for node in graph:
        if len(graph[node]) > 0:
            clean_graph[node] = graph[node]
            clean_coordinates[node] = coordinates[node]
    return clean_graph, clean_coordinates


if __name__ == "__main__":
    import sys

    # Handy argument parser, allow to call the script with automatic argument checking, for example:
    # ./osm_to_graph.py ressources/massy         # OK
    # ./osm_to_graph.py                          # "error: the following arguments are required: osmfile"
    # ./osm_to_graph.py --print ressources/massy # OK and print
    import argparse
    can = argparse.ArgumentParser()
    can.add_argument("osmfile", help="OSM file name")
    can.add_argument('-p', '--print', action='store_true', help="Print the graph")
    asked = can.parse_args()

    # We open a file, but we could have get the data from elsewhere.
    with open(asked.osmfile, encoding="utf-8") as data:
        # Parse the XML stream.
        g,c = parse(data)

    # Clean useless nodes.
    graph,coordinates = clean(g,c)


    # An example of pretty printing the graph as coordinates only.
    if asked.print:
        for node in graph:
            lon,lat = coordinates[node]["lon"], coordinates[node]["lat"]
            print("({lon},{lat})".format(lon=lon,lat=lat), end=" : [")
            for neighbor in graph[node]:
                lon,lat = coordinates[neighbor]["lon"], coordinates[neighbor]["lat"]
                print("({lon},{lat})".format(lon=lon,lat=lat), end=", ")
            print("]",end="\n")

    # Log message are better printed on the secondary output stream.
    print(len(graph.keys()),"nodes", file=sys.stderr)

