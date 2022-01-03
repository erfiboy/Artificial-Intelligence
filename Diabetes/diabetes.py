import pandas as pd
from math import log2
import numpy as np
import graphviz
from csv import reader
from copy import deepcopy 

class Node:
    
    def __init__(self, parent, decision, interval, child = []):
        self.parent_ = parent
        self.decision_ = decision
        self.decision_interval_ = interval
        self.child_ = child
        self.name_ = ""

    def append_child(self, child):
        self.child_.append(child)
        
    def set_name(self, name):
        self.name_ = name

""" parsing the data 
"""
data = pd.read_csv('diabetes.csv', sep=',')
col_list = list(data.columns)

df = pd.read_csv('diabetes.csv', sep=',', usecols=col_list)

""" parse train data
"""
train_data =  []

for element in col_list:
    train_data.append(df[element].values.tolist())

np_data = np.zeros(shape=(len(train_data), len(train_data[0])))
for i in range(len(train_data)):
        np_data[i] = np.array(train_data[i])
   
# """ parse test data 
# """   
# total_number_of_persons = len(df)
# first_test_person_index = int(fraction_of_train_data * total_number_of_persons) + 1

# test_data = []

# with open('diabetes.csv','r') as f:
#     csv_reader = reader(f)
#     index = 0 
#     for row in csv_reader:
#         if index < first_test_person_index:
#             index += 1
#             continue
#         test_data.append(row)
#         index += 1

# a = 10
""" discretize data by divide the maximum and minimum of the 
    array into number of intervals
"""
def discretize_data():  
    number_of_intervals = 10
    index = 0
    total_intervals = []
    for array in np_data:
        if index == len(np_data)-1:
            continue
        max_element = array.max()
        min_element = array.min()
        steps = np.zeros(number_of_intervals)
        step_size = (max_element - min_element)/number_of_intervals
        
        for i in range(number_of_intervals):
            steps[i] = min_element + i * step_size
            
        np_data[index] = np.digitize(array, bins=steps)
        # print(steps)
        index += 1
        total_intervals.append(steps)
    return total_intervals

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
def create_decision_tree(data, parent, col_header, interval, steps):
    goal_index = len(col_header) -1
    
    if calculate_entropy(data[len(data)-1]) == 0:
        if data[goal_index][0] == 1:
            decision = "Yes"
        else:
            decision = "No"
        
        node = Node(parent, decision, interval,[])
        parent.append_child(node)
        return 
    
    maximum_gain = 0
    chosen_attribute_index = 0
    clusters_indexes = []
    
    for attribute in col_header:
        if attribute == col_header[goal_index]:
            if len(col_header) == 1:
                return
            continue
        gain ,indexes = calculate_gain(data[col_header.index(attribute)], data[goal_index])
        if gain >= maximum_gain:
            maximum_gain = gain
            clusters_indexes = indexes
            chosen_attribute_index = col_header.index(attribute)
    
    node_type = col_header.pop(chosen_attribute_index)
    l = data.pop(chosen_attribute_index)
    
    interval_list = steps.pop(chosen_attribute_index).tolist()
    
    node = Node(parent, node_type, interval, [])
    parent.append_child(node)
    
    for indexes in clusters_indexes:
        child_data = divide_data_with_indexes(deepcopy(data), indexes)
        if int(l[indexes[0]])-1 == 0:
            interval = "[" + str(round(interval_list[0],2))+ ", " + str(round(interval_list[1],2)) + "]"
        else:
            interval = "[" + str(round(interval_list[int(l[indexes[0]])-2],2))+ ", " + str(round(interval_list[int(l[indexes[0]])-1],2)) + "]"
        create_decision_tree(child_data, node, col_header, interval, steps)
     
    return 

""" evaluate the trained decision tree 
"""
def evaluate_the_decison_tree(test_data, decision_tree_root, columns_header):
    number_of_success = 0
    number_of_fails = 0
    for data in test_data:
        result = find_answer(decision_tree_root, data, columns_header)
        if result == data[-1]:
            number_of_success += 1
        else:
            number_of_fails +=1
            
    return number_of_success, number_of_fails            
        
        
        
def find_answer(node , data, columns_header):
    if node.decision_ == "Yes":
        return 1
    elif node.decision_ == "No":
        return 0
    else:
        index = columns_header.index(node.decision_)
        for child in node.child_:
            if child.decision_interval_ == data[index]:
                find_answer(child, data, columns_header)
                break
        
""" Seperate train and test data 
    and reshape each data set 
"""        
def seperate_data(data, fraction_of_train_data):
    train_data = [[] for i in range(len(data))]
    index_of_first_test_data = int(fraction_of_train_data*len(data[0])) + 1
    test_data = [[] for i in range(int((1-fraction_of_train_data)*len(data[0])))]
    data = data.tolist()
    for i in range(len(data)):
        for j in range(len(data[0])): 
            if (j <= int( fraction_of_train_data * len(data[0]))):
                train_data[i].append(data[i][j])
            else:
                break
            
    for i in range(index_of_first_test_data, len(data[0])):
        for j in range(len(data)):
            test_data[i- index_of_first_test_data].append(data[j][i])
                
    return train_data, test_data                


""" Train the tree the evaluate the results  
"""
if __name__ == '__main__':
    root = Node(None, "root", '', [])
    fraction_of_train_data = 0.9
    # print(train_data[5])
    steps = discretize_data()
    # print(type(steps))
    train_data , test_data = seperate_data(np_data, fraction_of_train_data)
    
    create_decision_tree(deepcopy(train_data), root, deepcopy(col_list), '', steps)
    
    tree_root = root.child_[0]

    number_of_success , number_of_fails = evaluate_the_decison_tree(test_data, tree_root, deepcopy(col_list))

    print("number of fails :",number_of_fails)
    print("number of success :",number_of_success)

    stack = [root]

    dot = graphviz.Digraph('round-table', comment='The Round Table')  

    name = 'a'
    root.set_name(name)
    size = 0
    while stack != []:
        for child in stack[0].child_:
            if stack[0].name_ == 'a':
                name = chr(ord(name)+1)
                dot.node(child.name_, child.decision_)  
            else:
                name = chr(ord(name)+1)
                child.set_name(name)
                if child.decision_ == 'Age':
                    continue
                dot.node(child.name_, str(child.decision_interval_) + "\n" + child.decision_)  
                start = stack[0].name_ 
                end = child.name_
                # print(start, end)
                dot.edge((start), (end))
            
            stack.append(child)
        size += 1
        stack.pop(0)

    dot.render(directory='doctest-output', view= True).replace('\\', '/')