#!/usr/bin/env python
import math
import os
import sys
def euclideanDistance(instance1, instance2):
    distance = 0
    indexs = []
    for x in range(len(instance1[2])):
        if instance1[2][x] in instance2[2]:
            distance += pow((instance1[0][x] - instance2[0][instance2[2].index(instance1[2][x])]), 2)
        else:
            distance += pow((instance1[0][x]), 2)
        indexs.append(instance1[2][x])
    for x in range(len(instance2[2])):
        if instance2[2][x] not in indexs:
            distance += pow((instance2[0][x]), 2)
    return math.sqrt(distance)



trainingSet = []
for line in sys.stdin:
    trainingSet.append(eval(line))
#trainingSet = []
#f = open("/home/parallels/Downloads/knn/dataset_test_knn.txt", "r")
#for line in f:
#    z = eval(line)
#    trainingSet.append(z)
#f.close()
f = open("/home/parallels/Downloads/knn/test.txt","r")
for l in f:
    testInstance = eval(l)
f.close()
distances = []
for x in range(len(trainingSet)):
    dist = euclideanDistance(testInstance, trainingSet[x])
    #distances.append((trainingSet[x][1], dist))
    print((trainingSet[x][1], dist))
