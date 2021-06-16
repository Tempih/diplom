#!/usr/bin/env python
import sys
import os
import sklearn
data = []
for line in sys.stdin:
    data.append(line)
if 0.31622776601683794 in data[0][0]:
    f = open("/home/parallels/Downloads/traintarget1.txt","r")
else:
    f = open("/home/parallels/Downloads/traintarget2.txt","r")
target = []
for i in f:
    target.append(eval(line))
for i in data:
    o = []
    index = []
    for j in range(len(dataset[i][0])):
        if dataset[i][0][j] != 0:
            o.append(round(dataset[i][0][j], 5))
            index.append(j)
        print([o, target[i], index])








