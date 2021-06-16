#!/usr/bin/env python
import sys
import os
def compute_tf(word_dict):
    tf = {}
    for word, count in word_dict.items():
        tf[word] = count
    return tf
tf = []
for i in range(len(word_dict)):
    tf.append(compute_tf(word_dict[i]))
return tf


