#!/usr/bin/env python
import sys

def test_split(index, value, dataset, right1,left1):
    left, right = {"all":0,0:0,1:0,2:0,3:0,4:0},{"all":0,0:0,1:0,2:0,3:0,4:0}
    for row in dataset:
        if index in row[2]:
            if row[0][row[2].index(index)] < value:
                left["all"] +=1
                left[row[1]] += 1
                left1.append(dataset.index(row))
            else:
                right["all"] +=1
                right[row[1]] += 1
                right1.append(dataset.index(row))
        else:
            left["all"] += 1
            left[row[1]] += 1
    return left, right

def get_split(dataset):
    sravnenie = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    for index in range(3000):
        for row in sravnenie:
            right1 = []
            left1 = []
            groups = list(test_split(index, row, dataset, right1, left1))
            groups.append(row)
            groups.append(right1)
            groups.append(index)
            groups.append(left1)
            print(groups)
dataset = []
for line in sys.stdin:
    dataset.append(eval(line))
get_split(dataset)
