import pandas as pd
from math import log2
import numpy as np
import graphviz
import csv
from copy import deepcopy

class Node:
    
    def __init__(self, parent, decision, interval, gain, entropy ,child = []):
        self.name_ = ""
        self.child_ = child
        self.gain_ = gain
        self.entropy_ = entropy
        self.parent_ = parent
        self.decision_ = decision
        self.decision_interval_ = interval

    def append_child(self, child):
        self.child_.append(child)
        
    def set_name(self, name):
        self.name_ = name

""" parsing the numeric data for train dicision tree
"""
df = pd.read_csv('restaurant.csv')
col_list = list(df.columns)

df = pd.read_csv('restaurant.csv', sep=',', usecols=col_list)
wait_data =  []
for element in col_list:
    wait_data.append(df[element].values.tolist())
 
""" parsing phonetic data for visualization
""" 
df1 = pd.read_csv('names.csv')
column = list(df1.columns)

df = pd.read_csv('names.csv', sep=',', usecols=column)
name_of_data =  []
for element in column:
    name_of_data.append(df[element].values.tolist())
    
""" calculating entropy of the input data
    Note: data should be numeric
"""
def calculate_entropy(data):
    # find unique values 
    unique_values = set(data)
    probabilities = []
    for elements in unique_values:
        probabilities.append(data.count(elements)/len(data))
    
    entropy = 0 
    for probability in probabilities:
        entropy -= probability*log2(probability)
    
    return entropy

""" clustring data to compute the entrpy after pic that attribute 
    for decision tree node
"""
def cluster_data(data, goal):
    unique_values = set(data)
    clusters = []
    indexes = []
    for unique_value in unique_values:
        cluster = []
        index = []
        counter = 0
        
        for _data in data:
            if _data == unique_value:
                cluster.append(goal[counter])
                index.append(counter)
            counter += 1
        
        clusters.append(cluster)   
        indexes.append(index) 
        
    return clusters , indexes


""" calculating the remainder 
"""
def calculate_remainder(data, goal):
    clustered_data, indexes = cluster_data(data, goal)
    remainder = 0
    for cluster in clustered_data:
        remainder += (len(cluster)/len(data)) * calculate_entropy(cluster)
    
    return remainder , indexes

""" calculating the gain base on a data clustring 
"""
def calculate_gain(data, goal):
    data_entropy_before_clustering = calculate_entropy(goal)
    remainder, indexes = calculate_remainder(data, goal)
    return data_entropy_before_clustering - remainder , indexes , data_entropy_before_clustering

""" make the data ready for the next clusters or layers of the tree
"""
def divide_data_with_indexes(data, index):
    divided_data = []
    for i in range(len(data)):
        row = []
        for j in index:
            row.append(data[i][j])
        divided_data.append(row)
        
    return divided_data

""" create a disicion tree
"""
def create_decision_tree(data, name_data, parent, col_header, interval):
    goal_index = len(col_header) -1
    
    if calculate_entropy(data[len(data)-1]) == 0:
        if data[goal_index][0] == 1:
            decision = "Yes"
        else:
            decision = "No"
        
        node = Node(parent, decision, interval, 0, 0, [])
        parent.append_child(node)
        return 
    
    maximum_gain = 0
    maximum_entropy = 0
    choosen_attribute_index = ""
    clusters_indexes = []
    
    for attribute in col_header:
        if attribute == col_header[goal_index]:
            continue
        gain ,indexes ,entropy = calculate_gain(data[col_header.index(attribute)], data[goal_index])
        if gain > maximum_gain:
            maximum_gain = gain
            maximum_entropy = entropy
            clusters_indexes = indexes
            choosen_attribute_index = col_header.index(attribute)
    
    node_type = col_header.pop(choosen_attribute_index)
    data.pop(choosen_attribute_index)
    
    name_of_attribute = name_data.pop(choosen_attribute_index)
    
    node = Node(parent, node_type, interval, maximum_gain, maximum_entropy, [])
    parent.append_child(node)
    
    for indexes in clusters_indexes:
        child_data = divide_data_with_indexes(deepcopy(data), indexes)
        interval = name_of_attribute[indexes[0]]
        child_name_data = divide_data_with_indexes(deepcopy(name_data), indexes)
        create_decision_tree(child_data, child_name_data, node, col_header, interval)
     
    return 


root = Node(None, "root", "", 0, 0, [])

create_decision_tree(wait_data, name_of_data, root, col_list, "")


stack = [root]

dot = graphviz.Digraph('round-table', comment='The Round Table')  

name = 'a'
root.set_name(name)

while stack != []:
    for child in stack[0].child_:
        if stack[0].name_ == 'a':
            name = chr(ord(name)+1)
            entropy = "\n" +"H(V) = " + str(round(child.entropy_,2)) 
            gain =  "\n" + "G(V) = " + str(round(child.gain_,2)) 
            dot.node(child.name_, child.decision_ + entropy  + gain) 
        else:
            name = chr(ord(name)+1)
            child.set_name(name)
            entropy = "\n" +"H(V) = " + str(round(child.entropy_,2)) 
            gain = "\n" + "G(V) = " + str(round(child.gain_,2))
            dot.node(child.name_, child.decision_ + entropy  + gain)  
            start = stack[0].name_ 
            end = child.name_
            print(start, end)
            dot.edge((start), (end), "(" + str(child.decision_interval_) + ")")
        stack.append(child)
    stack.pop(0)

dot.render(directory='doctest-output', view= True).replace('\\', '/')