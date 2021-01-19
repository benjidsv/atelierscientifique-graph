import xml.etree.ElementTree as et
import time

def GetGraphFrom(filepath):
    start = time.time()

    STRnodes, STRlinks = GetNodesAndLinksFrom(filepath)
    nodes, links = ConvertToNumbers(STRnodes, STRlinks)
    G = MakeGraphFrom(nodes, links)

    end = time.time()
    s = end - start
    print(f"Task completed successfully. It took {round(s // 60)}mn{round(s % 60)}s to complete the graph.")

    return G


def GetNodesAndLinksFrom(filepath, encoding="utf-8", nodestr="node", linkstr="way"):
    rawnodes = []
    rawlinks = []
    nodes = {}
    links = []

    with open(filepath, encoding='utf-8') as data:
        tree = et.parse(data)
        root = tree.getroot()
        for node in root.findall(nodestr):
            rawnodes.append((node))
        for link in root.findall(linkstr):
            rawlinks.append(link)

    for node in rawnodes:
        nodes[node.get("id")] = (node.get("lat"), node.get("lon"))

    for link in rawlinks:
        refs = []
        for ref in link.iter("nd"):
            refs.append(ref.attrib["ref"])
            links.append(refs)

    return nodes, links


def MakeGraphFrom(nodes, links):
    G = {}

    for nodeid in nodes:
        G[nodes[nodeid]] = []

    for link in links:
        length = len(link)
        for i in range(length):
            if i == 0:
                if nodes[link[1]] not in G[nodes[link[0]]]:
                    G[nodes[link[0]]].append(nodes[link[1]])
            elif i == (length - 1):
                if nodes[link[i - 1]] not in G[nodes[link[i]]]:
                    G[nodes[link[i]]].append(nodes[link[i - 1]])
            else:
                if nodes[link[i - 1]] not in G[nodes[link[i]]]:
                    G[nodes[link[i]]].append(nodes[link[i - 1]])
                if nodes[link[i - 1]] not in G[nodes[link[i]]]:
                    G[nodes[link[i]]].append(nodes[link[i + 1]])

    return G


def ConvertToNumbers(nodes, links):
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

    return convertednodes, convertedlinks