#!/usr/bin/env python
import sys
import os
f = open("/home/parallels/Downloads/sd", "r")
for line in f:
    root = eval(line)
f.close()
f = open("/home/parallels/Downloads/f1.txt", "w")
f.write(str(root['groups'][1][0]))
f.close()
f = open("/home/parallels/Downloads/f2.txt", "w")
f.write(str(root['groups'][1][1]))
f.close()
