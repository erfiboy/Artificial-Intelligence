import graphviz
import numpy as np
import pandas as pd
from csv import reader
from copy import deepcopy 
from math import log2, inf
import matplotlib.pyplot as plt
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
   
""" discretize data by divide the maximum and minimum of the 
    array into number of intervals
"""
def discretize_data(number_of_intervals, data):  
    index = 0
    total_intervals = []
    for array in data:
        if index == len(data)-1:
            continue
        max_element = array.max()
        min_element = array.min()
        steps = np.zeros(number_of_intervals)
        step_size = (max_element - min_element)/number_of_intervals
        
        for i in range(number_of_intervals):
            steps[i] = min_element + i * step_size
            
        data[index] = np.digitize(array, bins=steps)
        # print(steps)
        index += 1
        total_intervals.append(steps)
    return total_intervals, data

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

""" create a decision tree      
"""
def create_decision_tree(data, parent, col_header, interval, steps, depth):
    goal_index = len(col_header) -1
    
    # all data have the same classification
    if calculate_entropy(data[len(data)-1]) == 0:
        if data[goal_index][0] == 1:
            decision = "Yes"
        else:
            decision = "No"
        
        node = Node(parent, decision, interval, 0, 0, [])
        parent.append_child(node)
        return 
    
    maximum_gain = 0
    max_entropy = 0
    chosen_attribute_index = 0
    clusters_indexes = []
    
    for attribute in col_header:
        if attribute == col_header[goal_index]:
            if len(col_header) == 1:
                result =  data[-1]
                yes = result.count(1)
                total = len(data[-1])
                if yes >= total * 0.5:
                    result =  "Yes"
                else:
                    result = "No"
                node = Node(parent, result, interval, 0, calculate_entropy(result), [])
                parent.append_child(node)
                return
            continue
        gain ,indexes , entropy = calculate_gain(data[col_header.index(attribute)], data[goal_index])
        if gain >= maximum_gain:
            maximum_gain = gain
            max_entropy = entropy
            clusters_indexes = indexes
            chosen_attribute_index = col_header.index(attribute)
    
    if maximum_gain == 0:
        result =  data[-1]
        yes = result.count(1)
        total = len(data[-1])
        if yes >= total * 0.5:
            result =  "Yes"
        else:
            result = "No"
        node = Node(parent, result, interval, 0, calculate_entropy(result),[])
        parent.append_child(node)
        return
    
    node_type = col_header.pop(chosen_attribute_index)
    l = data.pop(chosen_attribute_index)
    
    interval_list = steps.pop(chosen_attribute_index).tolist()
    
    node = Node(parent, node_type, interval, maximum_gain, max_entropy, [])
    parent.append_child(node)
    
    for indexes in clusters_indexes:
        child_data = divide_data_with_indexes(deepcopy(data), indexes)
        if int(l[indexes[0]])-1 == 0:
            interval = str(round(interval_list[0],2))+ ", " + str(round(interval_list[1],2))
        else:
            if int(l[indexes[0]]) >= len(interval_list):
                str(round(interval_list[int(l[indexes[0]])-1],2))+ ", " + str(inf)
            else:
                interval = str(round(interval_list[int(l[indexes[0]])-1],2))+ ", " + str(round(interval_list[int(l[indexes[0]])],2))
        create_decision_tree(deepcopy(child_data), node, deepcopy(col_header), interval, deepcopy(steps), depth+1)
     
    return 

""" evaluate the trained decision tree 
"""
def evaluate_the_decison_tree(test_data, decision_tree_root, columns_header):
    number_of_success = 0
    number_of_fails = 0
    for data in test_data:
        result = find_answer(decision_tree_root, data, columns_header)
        if result == int(data[-1]):
            number_of_success += 1
        else:
            number_of_fails +=1
            
    return number_of_success, number_of_fails            
        
""" find yes or no for a specific data
"""          
def find_answer(node , data, columns_header):
    total_number_of_child = len(node.child_) -1
    if node.decision_ == "Yes":
        return 1
    elif node.decision_ == "No":
        return 0
    else:
        index = columns_header.index(node.decision_)
        child_number = 0
        for child in node.child_:
            Min = float(list(child.decision_interval_.split(","))[0])
            Max = float(list(child.decision_interval_.split(","))[1])
            if child_number == 0 and Min >= float(data[index]):
                return find_answer(child, data, columns_header)
            if  Min <= float(data[index]) and Max >= float(data[index]):
                return find_answer(child, data, columns_header)
            if child_number == total_number_of_child and float(data[index]) > Max:
                return find_answer(child, data, columns_header)
            child_number += 1
                
""" Seperate train and test data 
    and reshape each data set 
"""        
def seperate_data(data, fraction_of_train_data):
    train_data = [[] for i in range(len(data))]
    index_of_first_test_data = int(fraction_of_train_data*len(data[0])) + 1
    test_data = []
    data = data.tolist()
    for i in range(len(data)):
        for j in range(len(data[0])): 
            if (j <= int( fraction_of_train_data * len(data[0]))):
                train_data[i].append(data[i][j])
            else:
                break
            
    with open('diabetes.csv', 'r') as f:
        csv_dict_reader = reader(f)
        index = 0 
        for row in csv_dict_reader:
            if index < index_of_first_test_data:
                index += 1
                continue
            index += 1
            test_data.append(row)
                
    return train_data, test_data                

""" visualize graph with graphviz
"""
def visualize(root):
    stack = [root]
    tree_root = root.child_[0]
    number_of_success , number_of_fails = evaluate_the_decison_tree(test_data, tree_root, deepcopy(col_list))
    dot = graphviz.Digraph('round-table', comment='The Round Table')  
    name = 'a'
    root.set_name(name)
    size = 0
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
                dot.edge((start), (end), "(" + str(child.decision_interval_) + ")")
            stack.append(child)
        size = size + 1
        stack.pop(0)
        
    success_rate = number_of_success/(number_of_fails+number_of_success)
    print("number of fails :",number_of_fails)
    print("number of success :",number_of_success)
    print("precente = " , success_rate, "%")
    print("Number of Nodes = ", size)
    
    dot.node("result ", " Success Rate = " + str(round(success_rate*100,3)) + "% \n" 
             + " total node size = " + str(size))
    
    dot.render(directory='doctest-output', view= True).replace('\\', '/')
    
""" test the trained data with different train 
    percentages and number of clustring 
"""
def plot_different_training():  
    number_of_child = [i+1 for i in range(40)]
    success_precentage = []
    for i in number_of_child:
        test_data = deepcopy(np_data)
        root = Node(None, "root", '', 0, 0, [])
        fraction_of_train_data = 0.7
        steps ,test_data = discretize_data(i, test_data)
        train_data , test_data = seperate_data(test_data, fraction_of_train_data)
        create_decision_tree(deepcopy(train_data), root, deepcopy(col_list), '', steps, 0)
        tree_root = root.child_[0]
        number_of_success , number_of_fails = evaluate_the_decison_tree(test_data, tree_root, deepcopy(col_list))
        success_precentage.append(number_of_success/(number_of_fails + number_of_success))
    
    plt.plot(number_of_child,success_precentage)
    plt.show()
    
    fraction_of_train_data_step = [i/100 for i in range(50,100,5)]
    success_precentage = []
    for i in fraction_of_train_data_step:
        test_data = deepcopy(np_data)
        root = Node(None, "root", '', 0, 0, [])
        fraction_of_train_data = i
        steps ,test_data = discretize_data(4, test_data)
        train_data , test_data = seperate_data(test_data, fraction_of_train_data)
        create_decision_tree(deepcopy(train_data), root, deepcopy(col_list), '', steps, 0)
        tree_root = root.child_[0]
        number_of_success , number_of_fails = evaluate_the_decison_tree(test_data, tree_root, deepcopy(col_list))
        success_precentage.append(number_of_success/(number_of_fails + number_of_success))
    
    plt.plot(fraction_of_train_data_step,success_precentage)
    plt.show()

""" Train the tree the evaluate the results  
"""
if __name__ == '__main__':
    
    root = Node(None, "root", '', 0, 0, [])
    fraction_of_train_data = 0.7
    steps, data = discretize_data(5, deepcopy(np_data))
    train_data , test_data = seperate_data(data, fraction_of_train_data)
    create_decision_tree(deepcopy(train_data), root, deepcopy(col_list), '', steps, 0)
    tree_root = root.child_[0]
    visualize(root)
    plot_different_training()
