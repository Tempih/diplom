#!/usr/bin/env python
import sys
import os

i = int(sys.argv[1])
test_data_tfidf = []
f = open("/home/parallels/Downloads/knn/dataset_test_knn_100.txt", "r")
for line in f:
    z = eval(line)
    test_data_tfidf.append(z)
f.close()
f = open("/home/parallels/Downloads/knn/test.txt","w")
f.write(str(test_data_tfidf[i]))
f.close()







