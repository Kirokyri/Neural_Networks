import os
from sys import argv
import math


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


def checkCycles(vertexList, adjList):
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
            if edge[0] == vertex:
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

# Подстановка операций в функцию графа
def substituteOperations(graphFunction, vertexList, opVertDict):
     for vertex in vertexList:
        graphFunction = graphFunction.replace(vertex, opVertDict[vertex])
     return graphFunction


def calculateGraphFunction(graphFunction):
     pos1 = graphFunction.rfind('(')
     if pos1 == -1:
         return graphFunction

     pos2 = graphFunction.find(')', pos1)
     operation = graphFunction[pos1 - 1 : pos1]
     opPos = pos1 - 1
     if operation == 'p':
         operation = graphFunction[pos1 - 3 : pos1]
         opPos = pos1 - 3

     values = graphFunction[pos1 + 1 : pos2].split(', ')
     if '+' in values or '*' in values or 'exp' in values:
         print('Ошибка вычисления. На месте одной из операций должно быть число.')
         return

     values = list(map(int, values))
     if operation == '+':
         newVal = sum(values, 0)
     elif operation == '*':
         newVal = math.prod(values)
     elif operation == 'exp':
         newVal = math.exp(values[0])

     graphFunction = graphFunction.replace(graphFunction[opPos : pos2 + 1], str(newVal))

     return calculateGraphFunction(graphFunction)


if len(argv) < 4:
    print('Не хватает входных аргументов.')
    exit(0)
inputFile = argv[1][7::]
operationsInputFile = argv[2][7::]
outputFile = argv[3][8::]

edges = parseTextFile(inputFile)
checkCorrectivity(edges)

vertexList = getVertexList(edges)
adjList = getAdjList(edges, vertexList)

checkCycles(vertexList, adjList)

collectorList = getCollectorList(edges, vertexList)

graphFunctionList = []
for collector in collectorList:
    graphFunction = str(collector)
    graphFunction = buildGraphFunction(collector, graphFunction)
    graphFunctionList.append(graphFunction)


with open(operationsInputFile, 'r') as file:
    operations = file.read().splitlines(False)

# Словарь соответствия вершин и операций
opVertDict = {}
for op in operations:
    vert, operation = op.split(':')
    vert = vert.strip(' ')
    operation = operation.strip(' ')
    opVertDict[vert] = operation


# Заменяем вершины на операции и значения в строке функции графа
graphOperationList = []
for fun in graphFunctionList:
    graphOperationList.append(substituteOperations(fun, vertexList, opVertDict))

with open(outputFile, 'w') as file:
    for i in range(len(graphOperationList)):
        file.write(f'{graphFunctionList[i]} -> {graphOperationList[i]} -> {calculateGraphFunction(graphOperationList[i])}\n')
