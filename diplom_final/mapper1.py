#!/usr/bin/env python
import sys
def test_split(index, value, dataset, right1,left1,rows):
    left, right = {"all":0,0:0,1:0,2:0,3:0,4:0},{"all":0,0:0,1:0,2:0,3:0,4:0}
    for row in rows:
        if index in dataset[row][2]:
            if dataset[row][0][dataset[row][2].index(index)] < value:
                left["all"] +=1
                left[dataset[row][1]] += 1
                left1.append(row)
            else:
                right["all"] +=1
                right[dataset[row][1]] += 1
                right1.append(row)
        else:
            left["all"] += 1
            left[dataset[row][1]] += 1
            left1.append(row)
    return left, right

def get_split(dataset):
    if dataset[0][0][0] == 0.31623:
        f = open("/home/parallels/Downloads/f1.txt","r")
        for l in f:
            rows = eval(l)
        f.close()
    else:
        f = open("/home/parallels/Downloads/f2.txt","r")
        for l in f:
            rows = eval(l)
        f.close()
    sravnenie = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    for index in range(3000):
        for row in sravnenie:
            right1 = []
            left1 = []
            groups = list(test_split(index, row, dataset, right1, left1,rows))
            groups.append(row)
            groups.append(right1)
            groups.append(index)
            groups.append(left1)
            print(groups)
dataset = []
indexs = []
for line in sys.stdin:
    z = eval(line)
    dataset.append(z)
get_split(dataset)
