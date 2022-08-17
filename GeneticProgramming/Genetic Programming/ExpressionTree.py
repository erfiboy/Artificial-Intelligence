import random
import math
import numpy as np
from decimal import Decimal
from math import sin, cos, pi, log
from numpy.random import choice
from copy import deepcopy
import sys
import time
start_time = time.time()
sys.float_info.max

class Node:

    def __init__(self, data, depth = 0):
        self.data_ = data
        self.left_ = None
        self.right_ = None
        self.depth_ = depth  

class ExpTree:
    
    def __init__(self, input_x_list = [], input_y_list = [] , initalpopulation = 200):
        self.inputxlist_ = input_x_list
        self.inputylist_ = input_y_list
        self.numberofiteration_ = 100
        self.numbernextgeneration_ = 20
        self.initalpopulation_ = initalpopulation
        self.roots_ = []
        self.fitnesses = []
        self.expressions = []
        self.numberoffitnesscalls = 0
        self.selectionMethods_ = ["Roulette wheel selection"]
        self.singleoprands_ = ['cos','sin']
        self.towoprands_ = ['*','+','-','/','*','+','-','/',"**"] 
    
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
            return str(root.data_)

        if self.is_single_operand(root.data_):
            right = self.create_expression_from_tree(root.right_)
            return str(root.data_) + "(" + str(right) + ")"

        if self.is_two_operand(root.data_):
            right = self.create_expression_from_tree(root.right_)
            left = self.create_expression_from_tree(root.left_)
            return "(" + str(left) + " " + str(root.data_) + " " + str(right) + ")"

    def evaluate_expretion(self, expression, x_list = None):
        if x_list == None:
            x_list = self.inputxlist_
        answer = []
        for x in x_list:
            try:
                answer.append(eval(expression))
            except ZeroDivisionError:
                answer.append(10e10)
                
        return answer

    def evaluate_tree_scores(self, root):
        answer = []
        for x in self.inputxlist_:
            try:
                result = self.evalaute_tree(root, x=x)
                if np.iscomplex(result):
                    self.roots_.pop(self.roots_.index(root))
                    return [10e10 for z in self.inputxlist_]        
                else:
                    answer.append(result)           
            except ZeroDivisionError:
                answer.append(10e2)
            except OverflowError:
                answer.append(10e2)
        return answer
                
    def evalaute_tree(self, root, x = 0):
        if root is None:
            return 0
        
        if self.is_leaf(root):
            if root.data_ == "x":
                return x
            return int(root.data_)

        if self.is_single_operand(root.data_):
            right = self.evalaute_tree(root.right_,x)
            if root.data_ == 'sin':
                return sin(right)
            elif root.data_ == 'cos':
                return sin(right)
            elif root.data_ == 'abs':
                return abs(right)

        if self.is_two_operand(root.data_):
            right = self.evalaute_tree(root.right_,x)
            left = self.evalaute_tree(root.left_,x)
            if root.data_ == '+':
                return left + right
            if root.data_ == '*':
                return left * right
            if root.data_ == '-':
                return left - right
            if root.data_ == '**':
                if (left > 10 and right > 5 or left > 3 and right > 10 or left > 8 and right > 8):
                    return 10e6
                return int(left) ** int(right)
            if root.data_ == '/':
                return left / right
    
    def fitness_function(self, list_y):
        mean_square_error = []
        self.numberoffitnesscalls += 1
        for i in range(len(list_y)):
            try:
                mean_square_error.append(int((list_y[i] - self.inputylist_[i])**2))
            except OverflowError:
                mean_square_error.append(10e6)
        return sum(mean_square_error)

    def selection(self):
        total_fitness_score = sum(self.fitnesses)
        probabilityـdistribution = [((total_fitness_score-fitness)/total_fitness_score)/(len(self.fitnesses)-1) for fitness in self.fitnesses]  
        self.roots_ = choice(self.roots_, self.numbernextgeneration_, p=probabilityـdistribution)
        
    def cross_over(self): 
        new_roots = [] 
        for i in range(len(self.roots_)):
            for j in range(i, len(self.roots_)):
                
                depth_to_cut_the_tree = random.randint(2, 3)
                left_tree_cut = choice(["r","l"], depth_to_cut_the_tree, p=[0.5, 0.5])
                
                depth_to_cut_the_tree = random.randint(2, 3)
                right_tree_cut = choice(["r","l"], depth_to_cut_the_tree, p=[0.5, 0.5])

                first_parent = deepcopy(self.roots_[i])
                second_parent = deepcopy(self.roots_[j])
                
                fitst_parent_cut = None
                second_parent_cut = None
                
                last_move_first = None
                last_move_second = None
                
                p = first_parent
                q = second_parent
                
                for node in left_tree_cut:
                    if node == "r" and p.right_ != None:
                        fitst_parent_cut = p
                        p = p.right_
                        last_move_first = node
                    elif node == "l" and p.left_ != None:
                        fitst_parent_cut = p
                        last_move_first = node
                        p = p.left_
                    else:
                        break
                
                for node in right_tree_cut:
                    if node == "r" and q.right_ != None:
                        second_parent_cut = q
                        q = q.right_
                        last_move_second = node
                    elif node == "l" and q.left_ != None:
                        second_parent_cut = q
                        q = q.left_
                        last_move_second = node
                    else:
                        break
                    
                if  last_move_first == "r":
                    if  last_move_second == "r":
                        (second_parent_cut.right_,fitst_parent_cut.right_) = (fitst_parent_cut.right_, second_parent_cut.right_)  
                    elif last_move_second == "l":
                        (second_parent_cut.left_,fitst_parent_cut.right_) = (fitst_parent_cut.right_, second_parent_cut.left_)  
                elif  last_move_first == "l":
                    if  last_move_second == "r":
                        (second_parent_cut.right_,fitst_parent_cut.left_) = (fitst_parent_cut.left_, second_parent_cut.right_)  
                    elif last_move_second == "l":
                        (second_parent_cut.left_,fitst_parent_cut.left_) = (fitst_parent_cut.left_, second_parent_cut.left_)  
                        
                new_roots.append(first_parent)   
                new_roots.append(second_parent)                       
   
        # transfer best fathers to the next generation
        last_generation_roots = []
        for root in self.roots_:
            last_generation_roots.append(root) 
        
        self.roots_ = new_roots
        self.roots_.extend(last_generation_roots)
   
    def mutatoin(self):
        number_of_mutaion = random.randint(1, len(self.roots_)/5)
        mutated_roots = choice(self.roots_, number_of_mutaion)
        for root in mutated_roots:
            
            depth_to_mutet_the_tree = random.randint(3, 10)
            direction = choice(["r","l"], depth_to_mutet_the_tree, p=[0.5, 0.5])

            p = root

            for node in direction:
                if node == "r" and p.right_ != None:
                    p = p.right_
                elif node == "l" and p.left_ != None:
                    p = p.left_
                else:
                    
                    if p.data_ in self.towoprands_:
                        while  True:
                            secure_random = random.SystemRandom()
                            random_data = secure_random.choice(self.towoprands_)
                            if p.data_ != random_data:
                                p.data_ = random_data
                                break
                            
                    elif p.data_ in self.singleoprands_:
                        while  True:
                            secure_random = random.SystemRandom()
                            random_data = secure_random.choice(self.singleoprands_)
                            if p.data_ != random_data:
                                p.data_ = random_data
                                break
                    
                    else:
                        if random.random() > 0.7 :
                            p.data_ = random.randint(1, 50)
                        else:
                            p.data_ = "x"
                    break
                      
    def generate_expression_tree(self, current_depth = 0, not_use_x = False, max_depth = 2):
        if current_depth > max_depth:
            return 
        progress_precentage = current_depth/max_depth
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
            if ((node.data_ == '-' ) and node.left_.data_ == 'x'):
                not_use_x = True
            node.right_ = self.generate_expression_tree(current_depth+1, not_use_x)
            return node
            
        else:
            if random.random() > 0.5 or not_use_x:
                node =  Node(str(random.randint(1,10))) 
            else:
                node =  Node('x') 
            return node

    def run_genetic_algorithm(self, first_generation_prob_distribution = [0.2,0.4,0.4]):
        tree_size = [i for i in range(len(first_generation_prob_distribution))]
        sizes = choice(tree_size, self.initalpopulation_, p=first_generation_prob_distribution)
        
        i=0
        # generate first population
        for i in range(self.initalpopulation_):
            self.roots_.append(self.generate_expression_tree(max_depth=sizes[i]))    
        
        for root in self.roots_:
            print(self.create_expression_from_tree(root))
                
        print("first generation ----------------------------")
        for i in range(self.numberofiteration_):
            # fitness
            self.fitnesses = []
            for root in self.roots_:       
                y_list = self.evaluate_tree_scores(root)
                score = self.fitness_function(y_list)
                self.fitnesses.append(score)

            min_score = min(self.fitnesses)
            if min_score == 0 or min_score < 2 :
                break
            print("choosen = ",self.create_expression_from_tree(self.roots_[self.fitnesses.index(min_score)])," and min is:" , min_score)    
            # selection
            self.selection()
            
            
            
            #crossover
            self.cross_over()
            
            print("/n" , " ---------------------------  " , "/n")
            
            for root in self.roots_:
                print(self.create_expression_from_tree(root))
            
            # mutation
            self.mutatoin()
        
        min_score = min(self.fitnesses)
        print("choosen = ",self.create_expression_from_tree(self.roots_[self.fitnesses.index(min_score)]), "in  round ",  i,"th and number of fittness calls is" , self.numberoffitnesscalls)    
        
              
                
                
x_input = [i*pi/2 for i in range(1,50)]
y_input = []
tree = ExpTree()
while True:
    print("This is Genetic Algorithm ! what can i do for you :")
    print("1. adjust the initial population : ")
    print("2. adjust the x list(default is 0 to 50 step of tow) ")
    print("3. adjust number of iterations: ")
    print("4. adjust the y list(default you will enter a function2) ")
    print("5. Run Algorithm: ")
    input_ = input("please enter a number: ")                
                                  
    if input_ == "1":
        tree.initalpopulation_ = int(input("enter intial population : "))                    
    
    elif input_ == "2":
        n = int(input("Enter number of elements : ")) 
        for i in range(0, n):
            ele = int(input("enter the element value : "))
        x_input.append(ele)    
    
    elif input_ == "3":
        tree.numberofiteration_ = int(input("enter  number of iterations : ")) 
    
    elif input_ == "4":
        n = int(input("Enter number of elements : ")) 
        for i in range(0, n):
            ele = int(input("enter the element value : "))
        y_input.append(ele)    
        
    elif input_ == "5":
        if x_input == []:
            x_input = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        if y_input == []:    
            function = input("enter the function : ") 
            y_input = [eval(function) for x in x_input]
        
        print("sample x is :" , x_input)
        print("corresponding y is :" , y_input)
        tree.inputxlist_ = x_input
        tree.inputylist_ = y_input
        start_time = time.time()
        tree.run_genetic_algorithm()
        print("---the program executed in %s seconds ---" % (time.time() - start_time))
        break
    else:
        print(" enter a correct number :) ")
        continue






