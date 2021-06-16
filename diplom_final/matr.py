#!/usr/bin/env python
import sys
import os
import sklearn
data = []
for line in sys.stdin:
    data.extend(line)
tfidf = TfidfTransformer(use_idf = True).fit(data)
train_data_tfidf = tfidf.transform(data)
print(train_data_tfidf)






