import os
from sys import argv
import xml.etree.cElementTree as ET
from xml.dom import minidom


def parseTextFile(fileName):
    if (not os.path.isfile(fileName)):
        print('Не удалось открыть файл.')
        exit(0)

    file = open(fileName, 'r')
    lines = file.readlines()
    matrixList = []
    for line in lines:
        _, mat = line.split(':')
        mat = mat.strip(' ')
        mat = mat.strip('\n')
        pos1 = 0
        pos2 = 0
        tmpMatrix = []
        floatFlag = False
        while True:
            pos1 = mat.find('[', pos2)
            pos2 = mat.find(']', pos1)
            if pos1 == -1 or pos2 == -1:
                break

            row = mat[pos1 + 1 : pos2]
            if floatFlag or '.' in row:
                floatFlag = True
                row = list(map(float, row.split(', ')))
            else:
                row = list(map(int, row.split(', ')))

            tmpMatrix.append(row)
        matrixList.append(tmpMatrix)

    return matrixList


def transmuteVector(vector):
    if '.' in vector:
        vector = list(map(float, vector.split(', ')))
    else:
        vector = list(map(int, vector.split(', ')))
    return vector


def rationalSigmoidFun(z):
    return z / (abs(z) + 1)


def calculate(matrixList, vector):
    errIdx = 0
    for layer in matrixList:
        errIdx += 1
        newVector = []
        for neuron in layer:
            val = 0
            if len(vector) < len(neuron):
                print(f'Длина входного вектора меньше количества весов нейрона в строке {errIdx} входного файла.')
                exit(0)
            for i in range(len(vector)):            # Вычисление суммы произведения весов нейронов на значения входного вектора
                try:
                    val += neuron[i] * vector[i]
                except IndexError:
                    print(f'Ошибка. Неверное число весов в строке {errIdx}.')
                    exit(0)
            val = rationalSigmoidFun(val)           # Применение функции активации
            newVector.append(val)
        vector = newVector

    return vector


if len(argv) < 5:
    print('Не хватает входных аргументов. Треубется 2 входных файла и 2 выходных.')
    exit(0)
inputFile = argv[1][7::]
vectorInputFile = argv[2][7::]
outputXML = argv[3][8::]
outputFile = argv[4][8::]

with open(vectorInputFile, 'r') as file:
    vector = file.read()
try:
    vector = transmuteVector(vector)
except:
    print('Ошибка в формате входного вектора. Преполагаемый формат: x1, x2, x3, x4')
    exit(0)

matrixList = parseTextFile(inputFile)
calcResult = calculate(matrixList, vector)

with open(outputFile, 'w') as file:
    file.write(', '.join(list(map(str, calcResult))))

root = ET.Element('network')
for layer in matrixList:
    layerVal = ' '.join(list(map(str, layer)))
    ET.SubElement(root, 'layer').text = layerVal

dom = minidom.parseString(ET.tostring(root))
tree = dom.toprettyxml(indent='\t')
with open(outputXML, 'w') as file:
    file.write(tree)