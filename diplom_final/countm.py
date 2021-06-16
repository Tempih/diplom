#!/usr/bin/env python
import sys
import os
data = []
for line in sys.stdin:
    data.append(line)
lists = []
for i in data:
    lists.append(i.split())
print(lists)




