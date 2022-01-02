import pandas as pd
from math import log2
import numpy as np
import graphviz
import csv

class Node:
    
    def __init__(self, parent, decision, child = []):
        self.parent_ = parent
        self.decision_ = decision
        self.child_ = child
        self.name_ = ""

    def append_child(self, child):
        self.child_.append(child)
        
    def set_name(self, name):
        self.name_ = name

""" parsing the data
"""
df = pd.read_csv('diabetes.csv')
col_list = list(df.columns)

df = pd.read_csv('diabetes.csv', sep=',', usecols=col_list)
wait_data =  []

for element in col_list:
    wait_data.append(df[element].values.tolist())
 
np_data = np.zeros(shape=(len(wait_data), len(wait_data[0])))
for i in range(len(wait_data)):
    np_data[i] = np.array(wait_data[i])
   
   
def discretize_data():  
    number_of_intervals = 10
    for j in range(len(np_data)):
        max_element = np_data[j].max()
        min_element = np_data[j].min()
        steps = np.zeros(number_of_intervals)
        step_size = (max_element - min_element)/number_of_intervals
        
        for i in range(number_of_intervals):
            steps[i] = min_element + i * step_size
            
        np.digitize(np_data[j], steps)
        print(steps)


discretize_data()
print(np_data[0])   
print("---------")
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

""" clustering data to compute the entropy after pic that attribute 
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

""" calculating the gain base on a data clustering 
"""

def calculate_gain(data, goal):
    data_entropy_before_clustering = calculate_entropy(goal)
    remainder, indexes = calculate_remainder(data, goal)
    return data_entropy_before_clustering - remainder , indexes

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

""" create a decision tree
"""

def create_decision_tree(data, parent, col_header):
    goal_index = len(col_header) -1
    
    if calculate_entropy(data[goal_index]) == 0:
        if data[goal_index][0] == 1:
            decision = "Yes"
        else:
            decision = "No"
        
        node = Node(parent, decision, [])
        parent.append_child(node)
        return 
    
    maximum_gain = 0
    chosen_attribute_index = ""
    clusters_indexes = []
    
    for attribute in col_header:
        if attribute == col_header[goal_index]:
            continue
        gain ,indexes = calculate_gain(data[col_header.index(attribute)], data[goal_index])
        if gain > maximum_gain:
            maximum_gain = gain
            clusters_indexes = indexes
            chosen_attribute_index = col_header.index(attribute)
    
    node_type = col_header.pop(chosen_attribute_index)
    data.pop(col_header.index(attribute))
    
    node = Node(parent, node_type, [])
    parent.append_child(node)
    
    for indexes in clusters_indexes:
        child_data = divide_data_with_indexes(data, indexes)
        create_decision_tree(child_data, node, col_header)
     
    return 


# root = Node(None, "root")

# create_decision_tree(wait_data, root, col_list)


# stack = [root]

# dot = graphviz.Digraph('round-table', comment='The Round Table')  

# name = 'a'
# root.set_name(name)
# size = 0
# while stack != []:
#     for child in stack[0].child_:
#         if stack[0].name_ == 'a':
#             name = chr(ord(name)+1)
#             dot.node(child.name_, child.decision_)  
#         else:
#             name = chr(ord(name)+1)
#             child.set_name(name)
#             dot.node(child.name_, child.decision_)  
#             start = stack[0].name_ 
#             end = child.name_
#             print(start, end)
#             dot.edge((start), (end))
        
#         stack.append(child)
#     size += 1
#     stack.pop(0)

# # dot.render(directory='doctest-output', view= True).replace('\\', '/')
# print("size = ", size)