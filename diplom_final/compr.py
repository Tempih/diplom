#!/usr/bin/env python
import sys
import os
def reduce1(arr):
    return {arr[0]:sum(arr[1])}
for line in sys.stdin:
    data = eval(line)
endlist = []
for i in data:
    if i[0]!='' and i[0]!='-':
        endlist.append(reduce1(i))
print(endlist)
