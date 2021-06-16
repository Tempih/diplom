#!/usr/bin/env python
import sys
import os
data = []
for line in sys.stdin:
    data.append(line)
lists = []
for i in data:
    lists.append(i.split())
f = open("/home/parallels/Downloads/sd","r")
for i in f:
    word_set = eval(i)
f.close()
for i in lists:
    a = dict.fromkeys(word_set, 0)
    for word in i:
        a[word] += 1
    print(list(a.values()))







