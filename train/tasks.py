import sklearn.datasets
import random
from diplom_web.celery import app
from celery import shared_task, group
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import json
import os
import time
import spacy
import string
import math
import pickle

spis_dir = []

@app.task
def create_task(form, max_features):
    global twenty_train,train_data_tfidf, vect, tfidf, twenty_test,z, twenty_test

    twenty_train = sklearn.datasets.fetch_20newsgroups(subset='train',
                                                       shuffle=True,
                                                       random_state=322,
                                                       categories=form)
    twenty_test = sklearn.datasets.fetch_20newsgroups(subset='test',
                                                      shuffle=True,
                                                      random_state=322,
                                                      categories=form)
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom/train.txt", "w")
    k = []
    for j in range(len(twenty_train.data)):
        f.write(str([twenty_train.data[j].replace('\n', ' ')]))
        f.write('\n')
        k.append(twenty_train.target[j])
        # f.write(str(data))
    for j in range(len(twenty_test.data)):
        f.write(str([twenty_test.data[j].replace('\n', ' ')]))
        f.write('\n')
    f.close()
    # f = open("/Users/artemmikhaylov/PycharmProjects/diplom/test.txt", "w")
    # k_test = []
    # for j in range(len(twenty_test.data)):
    #     f.write(str([twenty_test.data[j].replace('\n', ' ')]))
    #     f.write('\n')
    #     k_test.append(twenty_test.target[j])
    #     # f.write(str(data))
    # f.close()
    cmd = "hadoop fs -rm -R /vect_model"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /predict"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /test"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /vect"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /tf_idf"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /tf_idf_train"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /tf_idf_test"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /tfidf_model"
    os.system(cmd)
    cmd = "hadoop fs -mkdir /test"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /static"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /count"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /inputc"
    os.system(cmd)
    cmd = "hadoop fs -rm /static/value_test.txt"
    os.system(cmd)
    cmd = "hadoop fs -rm /static/value_tfidf_test.txt"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /test_count"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /vect_test"
    os.system(cmd)
    cmd = "hadoop fs -rm -R /tf_idf_test"
    os.system(cmd)
    cmd = "hadoop fs -mkdir /static"
    os.system(cmd)
    cmd = "hadoop fs -mkdir /inputc"
    os.system(cmd)
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/train.txt /inputc/"
    os.system(cmd)
    # cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/testtarget.txt /static/"
    # os.system(cmd)
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/test.txt /test/"
    os.system(cmd)
    target = []
    target.extend(twenty_train.target)
    target.extend(twenty_test.target)
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom/traintarget.txt", "w")
    f.write(str(target))
    f.close()
    # f = open("/Users/artemmikhaylov/PycharmProjects/diplom/testtarget.txt", "w")
    # f.write(str(list(twenty_test.target)))
    # f.close()
    value = twenty_test.data[0].replace('\n', ' ')
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/value_count_test.txt", "w")
    f.write(str(value))
    f.close()
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/value_count_test.txt /static/"
    os.system(cmd)
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/traintarget.txt /static/"
    os.system(cmd)
    # cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/testtarget.txt /static/"
    # os.system(cmd)
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom/n.txt", "w")
    f.write(str(len(twenty_train.data)+len(twenty_test.data)))
    f.close()
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/n.txt /static/"
    os.system(cmd)
    # f = open("/Users/artemmikhaylov/PycharmProjects/diplom/n_test.txt", "w")
    # f.write(str(len(twenty_test.data)))
    # f.close()
    # cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/n_test.txt /static/"
    # os.system(cmd)
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom/max_features.txt", "w")
    f.write(str(max_features))
    f.close()
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/max_features.txt /static/"
    os.system(cmd)
    value = twenty_train.data[0].replace('\n', ' ')
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/value_count.txt", "w")
    f.write(str(value))
    f.close()
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/value_count.txt /static/"
    os.system(cmd)
    cmd = "mapred streaming -input /inputc -output /count -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/countm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/countr.py -cacheFile 'hdfs://localhost:9000/static/value_count.txt#value'"
    os.system(cmd)
    value = os.popen("hdfs dfs -cat hdfs://localhost:9000/count/part-00000 | head -1").read()
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/value.txt", "w")
    f.write(value[:int(len(value)/2)])
    f.close()
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/value.txt /static/"
    os.system(cmd)
    cmd = "mapred streaming -input /count/part-00000 -output /vect_model -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/vectorm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/vectorr.py -cacheFile 'hdfs://localhost:9000/static/max_features.txt#max_features'"
    os.system(cmd)
    cmd = "mapred streaming -input /count/part-00000 -output /vect -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fitm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fitr.py -cacheFile 'hdfs://localhost:9000/vect_model/part-00000#vect' -cacheFile 'hdfs://localhost:9000/static/value.txt#value'"
    os.system(cmd)
    value = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/vect/part-00000 | head -1").read())
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/value_tfidf.txt", "w")
    f.write(str(value))
    f.close()
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/value_tfidf.txt /static/"
    os.system(cmd)
    cmd = "mapred streaming -input /vect/part-00000 -output /tfidf_model -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/tf_idf_m.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/tf_idf_r.py -cacheFile 'hdfs://localhost:9000/static/n.txt#n' -cacheFile 'hdfs://localhost:9000/static/value_tfidf.txt#value'"
    os.system(cmd)
    cmd = "mapred streaming -input /vect/part-00000 -output /tf_idf -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fit_tfm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fit_tfr.py -cacheFile 'hdfs://localhost:9000/tfidf_model/part-00000#tfidf' -cacheFile 'hdfs://localhost:9000/static/value_tfidf.txt#value' -cacheFile 'hdfs://localhost:9000/static/n.txt#n' -cacheFile 'hdfs://localhost:9000/static/traintarget.txt#target'"
    os.system(cmd)
    # cmd = "mapred streaming -input /test -output /test_count -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/countm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/countr.py -cacheFile 'hdfs://localhost:9000/static/value_count_test.txt#value'"
    # os.system(cmd)
    # value = os.popen("hdfs dfs -cat hdfs://localhost:9000/test_count/part-00000 | head -1").read()
    # f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/value_test.txt", "w")
    # f.write(value[:int(len(value) / 2)])
    # f.close()
    # cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/value_test.txt /static/"
    # os.system(cmd)
    # cmd = "mapred streaming -input /test_count/part-00000 -output /vect_test -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fitm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fitr.py -cacheFile 'hdfs://localhost:9000/vect_model/part-00000#vect' -cacheFile 'hdfs://localhost:9000/static/value_test.txt#value'"
    # os.system(cmd)
    # value = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/vect_test/part-00000 | head -1").read())
    # f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/value_tfidf_test.txt", "w")
    # f.write(str(value))
    # f.close()
    # cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/value_tfidf_test.txt /static/"
    # os.system(cmd)
    # cmd = "mapred streaming -input /vect_test/part-00000 -output /tf_idf_test -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fit_tfm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/fit_tfr.py -cacheFile 'hdfs://localhost:9000/tfidf_model/part-00000#tfidf' -cacheFile 'hdfs://localhost:9000/static/value_tfidf_test.txt#value' -cacheFile 'hdfs://localhost:9000/static/n_test.txt#n' -cacheFile 'hdfs://localhost:9000/static/testtarget.txt#target'"
    # os.system(cmd)
    cmd = "mapred streaming -input /tf_idf/part-00000 -output /tf_idf_train -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/splitm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/splitr.py"
    os.system(cmd)
    cmd = "mapred streaming -input /tf_idf/part-00000 -output /tf_idf_test -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/splittm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/splitr.py"
    os.system(cmd)
    value = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/tf_idf_train/part-00000 | head -1").read())
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/value_final.txt", "w")
    f.write(str(value))
    f.close()
    cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/value_final.txt /static/"
    os.system(cmd)
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "w")
    f.write(str([1,form,0,0,0]))
    index_of_data = random.randint(0, len(twenty_train.data) - 1)
    first_area = twenty_train.data[index_of_data]
    # second_area = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/tf_idf/part-00000 | head -"+str(index_of_data)+" | tail -1").read())
    third_area = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/tf_idf/part-00000 | head -"+str(index_of_data)+" | tail -1").read())
    # cmd = "mapred streaming -input /count/part-00000 -output /word_set -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/word_set_m.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/word_set_r.py"
    # os.system(cmd)
    # time.sleep(1)
    # cmd = "mapred streaming -input /count/part-00000 -output /word_set_3000 -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/word_set_3000_m.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/word_set_3000_r.py -cacheFile 'hdfs://localhost:9000/word_set/part-00000#word_set' -cacheFile 'hdfs://localhost:9000/static/max_features.txt#max_features'"
    # os.system(cmd)
    # count = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/count/sd | head -1").read())
    # f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/count.txt", "w")
    # f.write(str(count))
    # f.close()
    # cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/count.txt /static/"
    # os.system(cmd)
    # cmd = "mapred streaming -input /count/sd -output /tf_idf -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/matm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/matr.py -cacheFile 'hdfs://localhost:9000/word_set_3000/sd#word_set' -cacheFile 'hdfs://localhost:9000/static/n.txt#n' -cacheFile 'hdfs://localhost:9000/static/count.txt#counte'"
    # os.system(cmd)
    # cmd = 'rm /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/sd'
    # os.system(cmd)



    # cmd = "mapred streaming -input /tf_idf/sd -output /tff -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/addtm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/addtr.py -cacheFile 'hdfs://localhost:9000/static/traintarget.txt#target' -cacheFile 'hdfs://localhost:9000/static/value.txt#value' -cacheFile 'hdfs://localhost:9000/static/n.txt#n'"
    # os.system(cmd)

    # twenty_train = sklearn.datasets.fetch_20newsgroups(subset='train',
    #                                                    shuffle=True,
    #                                                    random_state=42,
    #                                                    categories=form)
    # twenty_test = sklearn.datasets.fetch_20newsgroups(subset='test',
    #                                                   shuffle=True,
    #                                                   random_state=42,
    #                                                   categories=form)
    # vect = CountVectorizer(max_features=max_features, stop_words='english')
    # vect.fit(twenty_train.data)
    # train_data = vect.transform(twenty_train.data)
    # tfidf = TfidfTransformer(use_idf=True).fit(train_data)
    # train_data_tfidf = tfidf.transform(train_data).A
    # index_of_data = random.randint(0, len(twenty_train.data)-1)
    # z = []
    # for i in range(len(train_data_tfidf)):
    #     o = []
    #     index = []
    #     for j in range(len(train_data_tfidf[i])):
    #         if train_data_tfidf[i][j] != 0:
    #             o.append((train_data_tfidf[i][j]))
    #             index.append(j)
    #     z.append([o, twenty_train.target[i], index])
    data = [first_area,str(third_area)]
    return data
@app.task
def random_data():
    f = open("/Users/artemmikhaylov/PycharmProjects/diplom/n.txt", "r")
    n = eval(f.read())
    f.close()
    index_of_data = random.randint(0, n-1)
    first_area = ''
    third_area = ''
    print(index_of_data)
    first_area = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/inputc/train.txt | head -"+str(index_of_data)+" | tail -1").read())
    third_area = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/tf_idf/part-00000 | head -"+str(index_of_data)+" | tail -1").read())
    data = [first_area,str(third_area)]
    return data
@app.task
def learning(status,par1,par2, laerning_stat):
    global spis_dir
    try:
        if status == 'Дерево решений' or status == '0' or status == '3':
            if laerning_stat == 1:
                for i in spis_dir:
                    cmd = "hadoop fs -rm -R /" + i
                    os.system(cmd)
            spis_dir = []
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "r")
            z = eval(f.read())
            f.close()
            time.sleep(1)
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "w")
            z[2] = 0
            f.write(str(z))
            f.close()
            spis_dir.append('map')
            cmd = "mapred streaming -input /tf_idf_train/part-00000 -output /map -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/mapper.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/reducer1.py -cacheFile 'hdfs://localhost:9000/static/max_features.txt#max_features' -cacheFile 'hdfs://localhost:9000/static/value_final.txt#value'"
            os.system(cmd)

            def to_terminal(group):
                return group.index(max(group))

            # Create child splits for a node or make terminal
            def split(node, max_depth, min_size, depth, z):
                global chet
                if depth == 1:
                    chet = 0
                chet += 1
                left = []
                right = []
                for j in node['groups'][0]:
                    left.extend(j)
                for j in node['groups'][1]:
                    right.extend(j)
                del (node['groups'])
                # check for a no split
                sum_l = 0
                sum_r = 0
                for i in range(5):
                    if node["pred"][0][i] == 0:
                        sum_l += 1
                for i in range(5):
                    if node["pred"][1][i] == 0:
                        sum_r += 1
                if not left or not right:
                    res = []
                    for i in range(5):
                        res.append(node["pred"][0][i] + node["pred"][1][i])
                    node['left'] = node['right'] = to_terminal(res)
                    return
                # check for max depth
                if depth >= max_depth:
                    node['left'], node['right'] = to_terminal(node["pred"][0]), to_terminal(node["pred"][1])
                    return
                # process left child
                if len(left) <= min_size or sum_l == 4:
                    node['left'] = to_terminal(node["pred"][0])
                else:
                    file_name = 'mapl' + str(depth) + 'l' + str(chet)
                    cmd = 'rm /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000'
                    os.system(cmd)
                    cmd = 'hadoop fs -get /' + z + '/part-00000 /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/'
                    os.system(cmd)
                    cmd = '/Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/l.py'
                    os.system(cmd)
                    spis_dir.append(file_name)
                    cmd = 'mapred streaming -input /tf_idf_train/part-00000 -output /' + file_name + " -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/mapper1.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/reducer.py -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f1.txt -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f2.txt -cacheFile 'hdfs://localhost:9000/static/max_features.txt#max_features' -cacheFile 'hdfs://localhost:9000/static/value_final.txt#value'"
                    os.system(cmd)
                    val = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/"+file_name+"/part-00000").read())
                    if val == 0:
                        cmd = "hadoop fs -rm -R /" + file_name
                        os.system(cmd)
                        cmd = 'mapred streaming -input /tf_idf_train/part-00000 -output /' + file_name + " -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/mapperb.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/reducer.py -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f1.txt -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f2.txt -cacheFile 'hdfs://localhost:9000/static/max_features.txt#max_features' -cacheFile 'hdfs://localhost:9000/static/value_final.txt#value'"
                        os.system(cmd)
                    cmd = 'rm /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000'
                    os.system(cmd)
                    cmd = 'hadoop fs -get /' + file_name + '/part-00000 /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/'
                    os.system(cmd)
                    f = open("/Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000", "r")
                    for line in f:
                        root = eval(line)
                    f.close()
                    node['left'] = root
                    split(node['left'], max_depth, min_size, depth + 1, file_name)
                    chet += 1
                # process right child
                if len(right) <= min_size or sum_r == 4:
                    node['right'] = to_terminal(node["pred"][1])
                else:
                    file_name = 'mapr' + str(depth) + 'r' + str(chet)
                    cmd = 'rm /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000'
                    os.system(cmd)
                    cmd = 'hadoop fs -get /' + z + '/part-00000 /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/'
                    os.system(cmd)
                    cmd = '/Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/r.py'
                    os.system(cmd)
                    spis_dir.append(file_name)
                    cmd = 'mapred streaming -input /tf_idf_train/part-00000 -output /' + file_name + " -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/mapper1.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/reducer.py -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f1.txt -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f2.txt -cacheFile 'hdfs://localhost:9000/static/max_features.txt#max_features' -cacheFile 'hdfs://localhost:9000/static/value_final.txt#value'"
                    os.system(cmd)
                    val = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/"+file_name+"/part-00000").read())
                    if val == 0:
                        cmd = "hadoop fs -rm -R /" + file_name
                        os.system(cmd)
                        cmd = 'mapred streaming -input /tf_idf_train/part-00000 -output /' + file_name + " -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/mapperb.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/reducer.py -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f1.txt -file /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/f2.txt -cacheFile 'hdfs://localhost:9000/static/max_features.txt#max_features' -cacheFile 'hdfs://localhost:9000/static/value_final.txt#value'"
                        os.system(cmd)
                    cmd = 'rm /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000'
                    os.system(cmd)
                    cmd = 'hadoop fs -get /' + file_name + '/part-00000 /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/'
                    os.system(cmd)
                    f = open("/Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000", "r")
                    for line in f:
                        root = eval(line)
                    f.close()
                    node['right'] = root
                    split(node['right'], max_depth, min_size, depth + 1, file_name)
                    chet += 1

            # {'index':b_index, 'value':b_value,'pred':[], 'groups':b_groups}
            cmd = 'rm /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000'
            os.system(cmd)
            cmd = 'hadoop fs -get /map/part-00000 /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/'
            os.system(cmd)
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/part-00000", "r")
            chet = 0
            for line in f:
                root = eval(line)
            f.close()
            split(root, int(par2), int(par1), 1, 'map')
            print(root)
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/asd", "w")
            f.write(str(root))
            f.close()
            cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/asd /static/"
            os.system(cmd)
            for i in spis_dir:
                cmd = "hadoop fs -rm -R /" + i
                os.system(cmd)
            # text_clf1 = DecisionTreeClassifier(criterion="gini",
            #                                    random_state=18,
            #                                    max_depth=int(par2),
            #                                    min_samples_leaf=int(par1),
            #                                    )
        elif status == 'k Ближайших Соседей':
            text_clf1 = KNeighborsClassifier(n_neighbors=int(par1),
                                             metric='cosine')
        # text_clf = text_clf1.fit(train_data_tfidf, twenty_train.target)
        f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "w")
        z[2] = 1
        f.write(str(z))
        f.close()
    except FileNotFoundError:
        print(spis_dir)
    return True

@app.task
def prediction(text_for_vect, status, par1, metod):
    global vect
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    if status == '0':
        cmd = "rm part-00000"
        os.system(cmd)
        cmd = "hadoop fs -get /vect_model/part-00000"
        os.system(cmd)
        f = open('/Users/artemmikhaylov/PycharmProjects/diplom_web/part-00000', 'r')
        vect_model = pickle.loads(eval(f.read()))
        f.close()
        cmd = "rm part-00000"
        os.system(cmd)
        cmd = "hadoop fs -get /tfidf_model/part-00000"
        os.system(cmd)
        f = open('/Users/artemmikhaylov/PycharmProjects/diplom_web/part-00000', 'r')
        tfidf_model = pickle.loads(eval(f.read()))
        f.close()
        cmd = "rm part-00000"
        os.system(cmd)
        data = [text_for_vect]
        lists = []
        for i in data:
            z = ""
            time_list = i.split()
            table = str.maketrans('', '', string.punctuation)
            for w in time_list:
                z += ' ' + w.translate(table)
            lists.append([z])
        top_list = []
        for i in lists:
            doc = nlp(i[0])
            time_list = [" ".join([token.lemma_ for token in doc])]
            fg = ([word.lower() for word in time_list[0].split() if word.isalpha()])
            text = ''
            for i in fg:
                text += i + ' '
            top_list.append(text.strip())
        vect_data = vect_model.transform(top_list)
        tfidf_data = tfidf_model.transform(vect_data).A.tolist()
        index = []
        values = []
        for j in range(len(tfidf_data[0])):
            if tfidf_data[0][j] != 0:
                values.append(tfidf_data[0][j])
                index.append(j)
        tf_idf = [values, index]
        def predict(node, row):
            if node['index'] in row[1]:
                if row[0][row[1].index(node['index'])] < node['value']:
                    if isinstance(node['left'], dict):
                        return predict(node['left'], row)
                    else:
                        return node['left']
                else:
                    if isinstance(node['right'], dict):
                        return predict(node['right'], row)
                    else:
                        return node['right']
            else:
                if isinstance(node['left'], dict):
                    return predict(node['left'], row)
                else:
                    return node['left']

        if metod == 'Дерево решений':
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/asd", "r")
            root = eval(f.read())
            f.close()
            result = predict(root, tf_idf)
        elif metod == 'k Ближайших Соседей':
            tf_idf.insert(1, 0)
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom/tf_idf_pred.txt",'w')
            f.write(str(tf_idf))
            f.close()
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom/k.txt",'w')
            par1.split()
            f.write(str(par1))
            f.close()
            cmd = "hadoop fs -rm /static/k.txt"
            os.system(cmd)
            cmd = "hadoop fs -rm /static/tf_idf_pred.txt"
            os.system(cmd)
            cmd = "hadoop fs -rm -R /knn_testtt"
            os.system(cmd)
            cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/tf_idf_pred.txt /static/"
            os.system(cmd)
            cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/k.txt /static/"
            os.system(cmd)
            cmd = 'mapred streaming -input /tf_idf_train/part-00000 -output /knn_testtt -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/knn/mapper.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/knn/reducer.py -cacheFile "hdfs://localhost:9000/static/tf_idf_pred.txt#test" -cacheFile "hdfs://localhost:9000/static/k.txt#k"'
            os.system(cmd)
            result = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/knn_testtt/part-00000").read())[0]

        # vect_text = vect.transform([str(text_for_vect)])
        # tfidf_text = tfidf.transform(vect_text)
        # pred_text = text_clf.predict(tfidf_text) mapred streaming -input /tff/part-00000 -output /knn_test -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/knn/mapper.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/knn/reducer.py -cacheFile "hdfs://localhost:9000/tf_idf/part-00000#test" -cacheFile "hdfs://localhost:9000/static/k.txt#k"
        # result = int(pred_text[0])
        return result
    elif status == '1':
        if metod == 'Дерево решений':
            cmd = "hadoop fs -rm -R /tree_result"
            os.system(cmd)
            cmd = 'mapred streaming -input /tf_idf_test/part-00000 -output /tree_result -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/predict_m.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/predict_r.py -cacheFile "hdfs://localhost:9000/static/asd#root"'
            os.system(cmd)
            result = os.popen("hdfs dfs -cat hdfs://localhost:9000/tree_result/part-00000").read().split('\n')
            print()
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "r")
            z = eval(f.read())
            f.close()
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "w")
            z[3] = 1
            f.write(str(z))
            f.close()
            return [eval(result[0]), eval(result[1])]
        elif metod == 'k Ближайших Соседей':
            cmd = "hadoop fs -rm /static/k.txt"
            os.system(cmd)
            cmd = "hadoop fs -rm -R /knn_test_full"
            os.system(cmd)
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom/k.txt", 'w')
            par1.split()
            f.write(str(par1))
            f.close()
            cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom/k.txt /static/"
            os.system(cmd)
            cmd = 'mapred streaming -input /tf_idf_train/part-00000 -output /knn_test_full -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/knn/mapper.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/knn/reducer.py -cacheFile "hdfs://localhost:9000/tf_idf_test/part-00000#test" -cacheFile "hdfs://localhost:9000/static/k.txt#k"'
            os.system(cmd)
            cmd = "rm part-00000"
            os.system(cmd)
            cmd = "hadoop fs -get /knn_test_full/part-00000"
            os.system(cmd)
            res = []
            f = open('/Users/artemmikhaylov/PycharmProjects/diplom_web/part-00000', 'r')
            for line in f:
                res.append(eval(line))
            f.close()
            trans_result = list(map(list, zip(*res)))
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "r")
            z = eval(f.read())
            f.close()
            f = open("/Users/artemmikhaylov/PycharmProjects/diplom_web/check.txt", "w")
            z[4] = par1
            f.write(str(z))
            f.close()
            return [(metrics.recall_score(trans_result[0], trans_result[1],average="weighted"))*100, (metrics.precision_score(trans_result[0], trans_result[1],average="weighted"))*100]
        # cmd = "hadoop fs -put /Users/artemmikhaylov/PycharmProjects/diplom_web/test_count.txt /static/"
        # os.system(cmd)
        # cmd = "mapred streaming -input /test_count/part-00000 -output /test_tf_idf -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/matm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/matr.py -cacheFile 'hdfs://localhost:9000/word_set_3000/part-00000#word_set' -cacheFile 'hdfs://localhost:9000/static/n.txt#n' -cacheFile 'hdfs://localhost:9000/static/test_count.txt#counte'"
        # os.system(cmd)
        #
        # cmd = "mapred streaming -input /test_tf_idf/part-00000 -output /test_tff -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/addtm.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/addtr.py -cacheFile 'hdfs://localhost:9000/static/testtarget.txt#target' -cacheFile 'hdfs://localhost:9000/static/n_test.txt#n'"
        # os.system(cmd)

        # cmd = "mapred streaming -input /test_tff/part-00000 -output /predict -mapper /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/predict_m.py -reducer /Users/artemmikhaylov/PycharmProjects/diplom/diplom_final/predict_r.py -cacheFile 'hdfs://localhost:9000/static/asd#root'"
        # os.system(cmd)
    #     result = eval(os.popen("hdfs dfs -cat hdfs://localhost:9000/predict/part-00000").read())
    #
    #     vect_text = vect.transform(twenty_test.data)
    #     tfidf_text = tfidf.transform(vect_text)
    #     prediction = text_clf.predict(tfidf_text)
    #     result = (metrics.accuracy_score(twenty_test.target, prediction)) * 100
    #     return result
@app.task
def del_dir():
    print(spis_dir)
    cmd = "hadoop fs -rm -R /" + spis_dir[-1]
    os.system(cmd)
