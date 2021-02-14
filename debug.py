import time
import xml.etree.ElementTree as et

def debugConverterPerformanceComparator(file, iteration, showMessage = True):
    timeConverterV1 = 0
    timeConverterV2 = 0
    isGraphsEquals = True
    
    printMsg("=============== START FILE CONVERSION BENCHMARK ================", showMessage)
    for i in range(iteration):
        (timeC1, graph1) = debugOldConverterPerformance(file, False)
        timeConverterV1 += timeC1
        (timeC2, graph2) = debugConverterPerformance(file, False)
        timeConverterV2 += timeC2
        if graph1 != graph2:
            isGraphsEquals = False
        
    printMsg(("Is graphs equals ? -" + str(isGraphsEquals)), showMessage)  
    printMsg(("Time need fo Converter V1 to do " + str(iteration) + " iterations = " + str(timeConverterV1) + "s average = " + str(timeConverterV1/iteration) + "s"), showMessage)
    printMsg(("Time need fo Converter V2 to do " + str(iteration) + " iterations = " + str(timeConverterV2) + "s average = " + str(timeConverterV2/iteration) + "s"), showMessage)
    
    printMsg(("total difference for " + str(iteration) + " iterations = " + str(abs(timeConverterV2-timeConverterV1)) + "s average substraction = " + str(abs((timeConverterV2/iteration) - (timeConverterV1/iteration))) + "s"), showMessage)
    printMsg("================================================================", showMessage)

    return None

def debugConverterPerformance(file, showMessage = True):
    printMsg("=================== START FILE CONVERSION V2 ===================", showMessage)
    startTime = time.time()
    graph = ConversionToGraphV2(file)
    endTime = time.time() - startTime
    printMsg(("Took : " + str(endTime) + " seconds to make a graph from the file."), showMessage)
    printMsg("================================================================", showMessage)
    return (endTime, graph)

def debugOldConverterPerformance(file, showMessage = True):
    printMsg("=================== START FILE CONVERSION V1 ===================", showMessage)
    startTime = time.time()
    graph = ConversionToGraphV1(file)
    endTime = time.time() - startTime
    printMsg(("Took : " + str(endTime) + " seconds to make a graph from the file."), showMessage)
    printMsg("================================================================", showMessage)
    return (endTime, graph)

def printMsg(message, showMessage = True):
    if showMessage :
        print(message)

def ConversionToGraphV2(file):
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

def ConversionToGraphV1(file):
    rawnodes = []
    rawlinks = []
    nodes = {}
    links = []

    with open(file, encoding='utf-8') as data:
        tree = et.parse(data)
        root = tree.getroot()
        for node in root.findall("node"):
            rawnodes.append((node))
        for link in root.findall("way"):
            rawlinks.append(link)

    for node in rawnodes:
        nodes[node.get("id")] = (node.get("lat"), node.get("lon"))

    for link in rawlinks:
        refs = []
        for ref in link.iter("nd"):
            refs.append(ref.attrib["ref"])
            links.append(refs)
    convertednodes = {}
    convertedlinks = []

    for nodeid in nodes:
        convertedid = int(nodeid)
        convertednodes[convertedid] = (float(nodes[nodeid][0]), float(nodes[nodeid][1]))

    convertedlink = []
    for link in links:
        if convertedlink != []:
            convertedlinks.append(convertedlink)
        convertedlink = []
        for nodeid in link:
            convertedlink.append(int(nodeid))
    nodes = convertednodes
    links = convertedlinks
    
    graph = {}
    for nodeid in nodes:
        graph[nodes[nodeid]] = []
    
    for link in links:
        length = len(link)
        
        for i in range(length):
            if i == 0:
                if nodes[link[1]] not in graph[nodes[link[0]]]:
                    graph[nodes[link[0]]].append(nodes[link[1]])
            elif i == (length - 1):
                if nodes[link[i - 1]] not in graph[nodes[link[i]]]:
                    graph[nodes[link[i]]].append(nodes[link[i - 1]])
            else:
                if nodes[link[i - 1]] not in graph[nodes[link[i]]]:
                    graph[nodes[link[i]]].append(nodes[link[i - 1]])
                if nodes[link[i + 1]] not in graph[nodes[link[i]]]:
                    graph[nodes[link[i]]].append(nodes[link[i + 1]])
    return graph


    
