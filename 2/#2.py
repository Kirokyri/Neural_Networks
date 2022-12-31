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


def getAdjList(edges, vertexList):
    adjList = {}
    for vertex in vertexList:
        tmp = []
        for edge in edges:
            if edge[1] == vertex and edge[0] not in tmp:
                tmp.append(edge[0])
        adjList[vertex] = tmp

    return adjList


def dfs(v, colors, d):
    colors[v] = 'grey'
    for y in d[v]:
        if colors[y] == 'white':
            dfs(y, colors, d)
        if colors[y] == 'grey':
            print('В графе присутствует цикл.')
            exit(0)
    colors[v] = 'black'


def checkCycles(vertexList, adjList):       # Используется обход в глубину
    colors = {}
    for vertex in vertexList:
        colors[vertex] = 'white'
    for vertex in vertexList:
        dfs(vertex, colors, adjList)
    
    return True


def getCollectorList(edgeList, vertexList):
    collectorsList = []
    for vertex in vertexList:
        flag = True
        for edge in edgeList:
            if edge[0] == vertex:       # Если из вершины выходит дуга, то она не является стоком
                flag = False
        if flag:
            collectorsList.append(vertex)

    return collectorsList


def buildGraphFunction(vert, graphFunction):
    if len(adjList[vert]) == 0:
        return graphFunction

    graphFunction += '('
    i = 0
    for vertex in adjList[vert]:
        if i != 0:
            graphFunction += ', '
        graphFunction += str(vertex)
        graphFunction = buildGraphFunction(vertex, graphFunction)
        i += 1
    graphFunction += ')'

    return graphFunction


if (len(argv) < 3):
    print('Не хватает входных аргументов. Требуется входной файл и выходной файл.')
    exit(0)
inputFile = argv[1][7::]
outputFile = argv[2][8::]

edges = parseTextFile(inputFile)
checkCorrectivity(edges)

vertexList = getVertexList(edges)           # Список вершин
adjList = getAdjList(edges, vertexList)     # Список смежности

checkCycles(vertexList, adjList)            # Проверка на наличие циклов

collectorList = getCollectorList(edges, vertexList)     # Список стоков в графе
   

with open(outputFile, 'w') as file:
    for collector in collectorList:         # Для каждого стока выполняется построение функции
        graphFunction = str(collector)
        graphFunction = buildGraphFunction(collector, graphFunction)
        file.write(graphFunction + '\n')

