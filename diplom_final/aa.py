#!/usr/bin/env python
import sys
import os
#cmd ='mapred streaming -input /input -output /map -mapper /home/parallels/Downloads/mapper.py -reducer /home/parallels/Downloads/reducer1.py'
#os.system(cmd)

def to_terminal(group):
    return group.index(max(group))

# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth,z):
    global chet
    chet += 1
    left = []
    right = []
    for j in node['groups'][0]:
        left.extend(j)
    for j in node['groups'][1]:
        right.extend(j)
    del(node['groups'])
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
            res.append(node["pred"][0][i]+node["pred"][1][i])
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
        file_name = 'mapl'+str(depth)+'l'+str(chet)
        cmd = 'rm sd'
        os.system(cmd)
        cmd = 'hadoop fs -get /' + z + '/sd'
        os.system(cmd)
        cmd = './l.py'
        os.system(cmd)
        cmd = 'mapred streaming -input /input -output /'+file_name+' -mapper /home/parallels/Downloads/mapper1.py -reducer /home/parallels/Downloads/reducer.py -file f1.txt -file f2.txt'
        os.system(cmd)
        cmd = 'rm sd'
        os.system(cmd)
        cmd = 'hadoop fs -get /'+file_name+'/sd'
        os.system(cmd)
        f = open("/home/parallels/Downloads/sd", "r")
        for line in f:
            root = eval(line)
        f.close()
        node['left'] = root
        split(node['left'], max_depth, min_size, depth+1,file_name)
        chet += 1
    # process right child
    if len(right) <= min_size or sum_r == 4:
        node['right'] = to_terminal(node["pred"][1])
    else:
        file_name = 'mapr' + str(depth) + 'r' + str(chet)
        cmd = 'rm sd'
        os.system(cmd)
        cmd = 'hadoop fs -get /' + z + '/sd'
        os.system(cmd)
        cmd = './r.py'
        os.system(cmd)
        cmd = 'mapred streaming -input /input -output /' + file_name + ' -mapper /home/parallels/Downloads/mapper1.py -reducer /home/parallels/Downloads/reducer.py -file f1.txt -file f2.txt'
        os.system(cmd)
        cmd = 'rm sd'
        os.system(cmd)
        cmd = 'hadoop fs -get /' + file_name + '/sd'
        os.system(cmd)
        f = open("/home/parallels/Downloads/sd", "r")
        for line in f:
            root = eval(line)
        f.close()
        node['right'] = root
        split(node['right'], max_depth, min_size, depth+1, file_name)
        chet += 1

# {'index':b_index, 'value':b_value,'pred':[], 'groups':b_groups}

cmd ='rm sd'
os.system(cmd)
cmd ='hadoop fs -get /map/sd'
os.system(cmd)
f = open("/home/parallels/Downloads/sd","r")
chet = 0
for line in f:
    root = eval(line)
f.close()
split(root, 10, 4, 1, 'map')
print(root)
f = open("/home/parallels/Downloads/asd","w")
f.write(str(root))
f.close()
