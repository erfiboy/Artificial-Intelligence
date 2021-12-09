import random
import math
from math import sin, cos, pi
from numpy.random import choice

class Node:

    def __init__(self, data, depth = 0):
        self.data_ = data
        self.left_ = None
        self.right_ = None
        self.depth_ = depth
        

class ExpTree:
    
    def __init__(self, input_x_list = [], input_y_list = []):
        self.inputxlist_ = input_x_list
        self.inputylist_ = input_y_list
        self.numberofiteration_ = 10
        self.numbernextgeneration_ = 10
        self.roots_ = []
        self.fitnesses = []
        self.expressions = []
        self.selectionMethods_ = ["Roulette wheel selection"]
        self.singleoprands_ = ['cos','sin','abs']
        self.towoprands_ = ['*','+','-','/','**'] 
    
    def is_leaf(self, node):
        return node.left_ is None and node.right_ is None

    def is_two_operand(self, oprand):
        if oprand in self.towoprands_:
            return True
        return False
    
    def is_single_operand(self, oprand):
        if oprand in self.singleoprands_:
            return True
        return False

    def create_expression_from_tree(self, root):    
        if root is None:
            return 0
        
        if self.is_leaf(root):
            return (root.data_)

        if self.is_single_operand(root.data_):
            right = self.create_expression_from_tree(root.right_)
            return str(root.data_) + "(" + str(right) + ")"

        if self.is_two_operand(root.data_):
            right = self.create_expression_from_tree(root.right_)
            left = self.create_expression_from_tree(root.left_)
            return "(" + str(left) + " " + str(root.data_) + " " + str(right) + ")"

    def evaluate_expretion(self, expression, list_of_x):
            answer = []
            for x in list_of_x:
                answer.append(eval(expression))
            return answer

    def fitness_function(self, list_y):
        mean_square_error = []
        
        zip_object = zip(self.input_y_list_, list_y)
        for list1_i, list2_i in zip_object:
            mean_square_error.append((list1_i-list2_i)**2)
            
        return sum(mean_square_error)

    def selection(self):
        total_fitness_score = sum(self.fitnesses)
        probabilityـdistribution = []
        
        for fitness in self.fitnesses:
            probabilityـdistribution.append((total_fitness_score - fitness) / total_fitness_score)    
            
        self.roots_ = choice(self.roots_, self.numbernextgeneration_, p=probabilityـdistribution)
        
    def generate_expression_tree(self, current_depth = 0, not_use_x = False, max_depth = 4):
        progress_precentage = (current_depth/max_depth)
        rand = random.random()
        if rand < 0.4*(1 - progress_precentage):
            secure_random = random.SystemRandom()
            node =  Node(secure_random.choice(self.singleoprands_)) 
            node.right_ = self.generate_expression_tree(current_depth+1, not_use_x)
            return node
            
        elif rand > 0.4*(1 - progress_precentage) and progress_precentage <0.9:
            secure_random = random.SystemRandom()
            node =  Node(secure_random.choice(self.towoprands_)) 
            node.left_ = self.generate_expression_tree(current_depth+1, not_use_x)
            if ((node.data_ == '-' or node.data_ == '**') and node.left_.data_ == 'x') or node.data_ == '/':
                not_use_x = True
            node.right_ = self.generate_expression_tree(current_depth+1, not_use_x)
            return node
            
        else:
            if random.random() > 0.5 or not_use_x:
                node =  Node(str(random.randint(1,10))) 
            else:
                node =  Node('x') 
            return node

        
            

# create_expression_from_tree(root)

tree = ExpTree()

root = tree.generate_expression_tree()
javab = tree.create_expression_from_tree(root)
print(javab)

javab = "int(" + javab + ")"
print(javab)
x = 10
print(eval(javab))

print(tree.evaluate_expretion(tree.create_expression_from_tree(root), [10]))
print('The value of the expression tree is', tree.create_expression_from_tree(root))


