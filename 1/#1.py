import os
from sys import argv
import xml.etree.ElementTree as ET
import xml.dom.minidom


def parseTextFile(fileName):
    if (not os.path.isfile(fileName)):
        print('Не удалось открыть файл.')
        exit(0)

    file = open(fileName, 'r')
    text = file.read()
    text = text.replace('\t', ' ')
    text = text.replace('  ', ' ')
    edges = []
    for edge in text.split('), '):
        edge = edge.lstrip('(').split(', ')
        edges.append([edge[0], edge[1], int(edge[2].rstrip(')'))])

    return edges


def checkCorrectivity(edges):
    stringNum = 0
    for edge1 in edges:
        stringNum += 1
        for edge2 in edges:
            if edge1 != edge2:
                if edge1[0] == edge2[0] and edge1[1] == edge2[1]:
                    print('Ошибка формата. Строка: ', stringNum)
                    exit(0)
                if edge1[1] == edge2[1] and edge1[2] == edge2[2]:
                    print('Ошибка формата. Строка: ', stringNum)
                    exit(0)


def getVertexList(edges):
    edges.sort(key=lambda i: (i[1], i[2]))
    vertexes = []
    for edge in edges:
        if edge[0] not in vertexes:
            vertexes.append(edge[0])
        if edge[1] not in vertexes:
            vertexes.append(edge[1])
    vertexes.sort()
    return vertexes

def printGraphToXml(edges, outFileName):
    vertexes = getVertexList(edges)
    graph = ET.Element('graph')
    for vertex in vertexes:
        vert = ET.SubElement(graph, 'vertex')
        vert.text = vertex
    

    for edge in edges:
        arc = ET.SubElement(graph, 'arc')

        el1Val = ET.SubElement(arc, 'from')
        el1Val.text = edge[0]

        el2Val = ET.SubElement(arc, 'to')
        el2Val.text = edge[1]

        el3Val = ET.SubElement(arc, 'order')
        el3Val.text = str(edge[2])

    tree = ET.ElementTree(graph)
    tree.write(outFileName, encoding='utf-8', xml_declaration=True)

    dom = xml.dom.minidom.parse(outFileName)
    pretty_xml_as_string = dom.toprettyxml()
    with open(outFileName, 'w', encoding='utf-8') as file:
        file.write(pretty_xml_as_string)


if (len(argv) < 3):
    print('Не хватает входных аргументов. Требуется входной файл и выходной файл.')
    exit(0)
inputFile = argv[1][7::]
outputFile = argv[2][8::]

# Считывание дуг
edges = parseTextFile(inputFile)

# Проверка коррекности введенных дуг
checkCorrectivity(edges)

# Вывод в формате XML
printGraphToXml(edges, outputFile)

