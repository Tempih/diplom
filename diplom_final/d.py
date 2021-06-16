#!/usr/bin/env python
import sys
import os
import sklearn.datasets
categories = ['alt.atheism', 'comp.graphics', 'comp.sys.mac.hardware', 'sci.electronics', 'sci.med']

twenty_train = sklearn.datasets.fetch_20newsgroups(subset='train',
                                                   shuffle=True,
                                                   random_state=42,
                                                   categories = categories )
twenty_test = sklearn.datasets.fetch_20newsgroups(subset='test',
                                                  shuffle=True,
                                                  random_state=42,
                                                  categories = categories)
for i in range(2):
    k = []
    f = open("/home/parallels/Downloads/train"+(i+1)+".txt","w")
    for j in range(i*int(len(twenty_train.data) / 2),(i+1)*int(len(twenty_train.data) / 2)):
        f.write(str(twenty_train.data[j]))
        f.write('/n')
        k.append(twenty_train.target[j])
    f.close()
    cmd = "hadoop fs -put /train"+(i+1)+".txt /inputc/"
    os.system(cmd)
    f = open("/home/parallels/Downloads/traintarget"+(i+1)+".txt","w")
    f.write(str(k))
    f.close()
cmd = "mapred streaming -input /inputc -output /count -mapper /home/parallels/Downloads/countm.py -reducer /home/parallels/Downloads/countr.py"
os.system(cmd)
cmd = 'hadoop fs -get /count/sd'
os.system(cmd)
cmd = "mapred streaming -input /inputc -output /mat -mapper /home/parallels/Downloads/matm.py -reducer /home/parallels/Downloads/matr.py"
os.system(cmd)
cmd ='rm sd'
os.system(cmd)
cmd = 'hadoop fs -get /mat/sd'
os.system(cmd)
f = open("/home/parallels/Downloads/sd","r")
tf = []
for i in f:
    tf.append(eval(i))
for i in range(2):
    k = []
    f = open("/home/parallels/Downloads/tf_idf"+(i+1)+".txt","w")
    for j in range(i*int(len(tf) / 2),(i+1)*int(len(tf) / 2)):
        f.write(str(tf[j]))
        f.write('/n')
    f.close()
    cmd = "hadoop fs -put /tf_idf"+(i+1)+".txt /inputtf/"
    os.system(cmd)
cmd = "mapred streaming -input /inputtf -output /tff -mapper /home/parallels/Downloads/addtm.py -reducer /home/parallels/Downloads/addtr.py"
os.system(cmd)
cmd ='rm sd'
os.system(cmd)
cmd = 'hadoop fs -get /mat/sd'
os.system(cmd)
data = []
for i in f:
    data.append(eval(i))
for i in range(2):
    k = []
    f = open("/home/parallels/Downloads/dataset"+(i+1)+".txt","w")
    for j in range(i*int(len(data) / 2),(i+1)*int(len(data) / 2)):
        f.write(str(data[j]))
        f.write('/n')
    f.close()
    cmd = "hadoop fs -put /dataset"+(i+1)+".txt /input/"
    os.system(cmd)


