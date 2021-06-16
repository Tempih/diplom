#!/usr/bin/env python
import sys
def gini_index(row, classes):
    # count all samples at split point
    n_instances = row[0]["all"] + row[1]["all"]
    # sum weighted Gini index for each group
    gini = 0.0
    for group in range(2):
        size = float(row[group]["all"])
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = row[group][class_val] / size
            score += p * p
        # weight the group score by its relative size
        gini += (1.0 - score) * (size / n_instances)
    return gini
rasbienie1 = []
for line in sys.stdin:
    rasbienie1.append(eval(line))
rasbienie = []
class_values = [0,1,2,3,4]
b_index, b_value, b_score = 3000, 3000, 3000
sorted(rasbienie1, key=lambda i: i[4])
for i in rasbienie1:
    a = [{"all": 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, {"all": 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, 0, [], 0, []]
    a[0]["all"] += i[0]["all"]
    a[1]["all"] += i[1]["all"]
    a[0][0] += i[0][0]
    a[0][1] += i[0][1]
    a[0][2] += i[0][2]
    a[0][3] += i[0][3]
    a[0][4] += i[0][4]
    a[1][0] += i[1][0]
    a[1][1] += i[1][1]
    a[1][2] += i[1][2]
    a[1][3] += i[1][3]
    a[1][4] += i[1][4]
    a[2] = i[2]
    a[4] = i[4]
    a[3].append(i[3])
    a[5].append(i[5])
    for j in rasbienie1:
        if i[2] == j[2] and i[4] == j[4] and i != j:
            a[0]["all"] += j[0]["all"]
            a[1]["all"] += j[1]["all"]
            a[0][0] += j[0][0]
            a[0][1] += j[0][1]
            a[0][2] += j[0][2]
            a[0][3] += j[0][3]
            a[0][4] += j[0][4]
            a[1][0] += j[1][0]
            a[1][1] += j[1][1]
            a[1][2] += j[1][2]
            a[1][3] += j[1][3]
            a[1][4] += j[1][4]
            a[3].append(j[3])
            a[5].append(j[5])
            del(rasbienie1[rasbienie1.index(j)])
            break
    rasbienie.append(a)
    gini = gini_index(a, class_values)
    if gini < b_score:
            b_pred = []
            info = [a[0]["all"],a[1]["all"]]
            b_pred.append([a[0][0],a[0][1],a[0][2], a[0][3], a[0][4]])
            b_pred.append([a[1][0],a[1][1],a[1][2], a[1][3], a[1][4]])
            b_index, b_value, b_score = a[4], a[2], gini
            b_row = rasbienie.index(a)
    del(rasbienie1[rasbienie1.index(i)])
for i in range(2):
    for j in range(1413):
        if j not in rasbienie[b_row][5][i] and j not in rasbienie[b_row][3][i]:
            rasbienie[b_row][5][i].append(j)
info.append([len(rasbienie[b_row][5][0]),len(rasbienie[b_row][5][1]),len(rasbienie[b_row][3][0]),len(rasbienie[b_row][3][1])])
print({'index': b_index, 'value': b_value, 'pred':b_pred, 'groups': [rasbienie[b_row][5],rasbienie[b_row][3]],"info":info})

