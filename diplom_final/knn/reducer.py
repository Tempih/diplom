#!/usr/bin/env python
import operator
import os
import sys
def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedVotes[0][0])


distances = []
for line in sys.stdin:
    distances.append(eval(line))
f = open("/home/parallels/Downloads/knn/k_value.txt","r")
for l in f:
    k = eval(l)
f.close()
distances.sort(key=operator.itemgetter(1))
neighbors = []
for x in range(k):
    neighbors.append(distances[x][0])
getResponse(neighbors)







