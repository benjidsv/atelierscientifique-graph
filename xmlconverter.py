import xml.etree.ElementTree as et
import time
from debug import printMsg

def getGraphFromFile(file, showMessage = False):
    printMsg("=================== START FILE CONVERSION ===================", showMessage)
    startTime = time.time()
    graph = createGraph(file)
    printMsg(("Took : " + str(time.time() - startTime) + " seconds to make a graph from the file."), showMessage)
    printMsg("=============================================================", showMessage)
    return graph
  
def createGraph(file):
    graph = {}
    nodes = {}
    links = []
    tree = None
    root = None
    
    with open(file, encoding='utf-8') as data:
        tree = et.parse(data)
        root = tree.getroot()

    for rawNode in root.findall("node"):
        nodes[int(rawNode.get("id"))] = (float(rawNode.get("lat")), float(rawNode.get("lon")))
        graph[nodes[int(rawNode.get("id"))]] = []
        
    for rawLink in root.findall("way"):
        neighbors = []
        i = 0
        for neighbor in rawLink.iter("nd"):
            neighbors.append(nodes[int(neighbor.attrib["ref"])])
        links.append(neighbors)

    for link in links:
        length = len(link)

        for i in range(length):
            l = graph.get(link[i], [])
            
            if length > 1 and i == 0:
                if link[1] not in l:
                    graph[link[0]].append(link[1])
                    
            elif i == (length - 1):
                if link[length - 2] not in l:
                    graph[link[length - 1]].append(link[length - 2])

            else:
                if link[i - 1] not in l:
                    graph[link[i]].append(link[i - 1])
                if link[i + 1] not in l:
                    graph[link[i]].append(link[i + 1])
    
    return graph
