import sys
import numpy as np
import random as rand

class Algorithm():

    def __init__(self , visible_map, robot_location, battery_location):
        self.method_ = "blind"
        self.randomdest_ = []
        self.visible_map_ = visible_map
        self.robot_location_ = robot_location
        self.battery_location_ = battery_location
        self.posible_directions = [(0,1),(1,0),(-1,0),(0,-1)]
        self.visited_map_ = []
        self.huristic_map_ = [[0 for _ in range(len(self.visible_map_[0]))] for _ in range(len(self.visible_map_))]

    def update(self, method, visible_map, robot_location, battery_location):
        self.method_ = method
        self.visible_map_ = visible_map
        self.robot_location_ = robot_location
        self.battery_location_ = battery_location

    def set_map(self, visible_map ,visited_map):
        self.visible_map_ = visible_map
        self.visited_map_ = visited_map
        
    def set_method(self, method):
        self.method_ = method
        
    def set_robot_location(self, robot_location):
        self.robot_location_ = robot_location
                  
    def set_battery_location(self, battery_location):
        self.battery_location_ = battery_location               
    
    def exec(self):
        if self.method_ == "manhattan":
            return self.manhattan()
        elif self.method_ == "weightedmanhattan":
            return self.weightedmanhattan()    
        elif self.method_ == "blind":
            return self.blind()
        elif self.method_ == "bfs":
            return self.bfs()
            
    def is_there_any_posible_path(self,location):
        if self.visible_map_[location[0]][location[1]] == "obstacle":
            print("no pass found")
            return False

        rel_pos_neighbors = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for rel_pos_neighbor in rel_pos_neighbors:
            pos_neighbor = (rel_pos_neighbor[0] + location[0], rel_pos_neighbor[1] + location[1])
            if pos_neighbor[0] < len(self.visible_map_) and pos_neighbor[1] < len(self.visible_map_[0]) and pos_neighbor[0] >= 0 and pos_neighbor[1] >= 0:
                if self.visible_map_[pos_neighbor[0]][pos_neighbor[1]] !=  "obstacle":
                    return True
       
        return False

    # A* : h is equal to the manhattan distance between battry and robot
    def manhattan(self):
        path = []
        estimate_robot_location = self.robot_location_
        
        for rows in range(len(self.huristic_map_)):
            for column in range(len(self.huristic_map_[0])):
                position = (rows, column)

                if  self.visible_map_[position[0]][position[1]] == "obstacle":
                    self.huristic_map_[position[0]][position[1]] = 10e15
                    continue

                self.huristic_map_[position[0]][position[1]] = ((self.battery_location_[0] - position[0])**2 + (self.battery_location_[1] - position[1])**2)**0.5
                self.huristic_map_[position[0]][position[1]] += self.visited_map_[position[0]][position[1]] * 2
        
        last_move = (0,0)
        while(self.battery_location_ != estimate_robot_location):
            best_move = (0,0)
            lowest_cost = 10e15
            for direction in self.posible_directions:
                position = (estimate_robot_location[0] + direction[0], estimate_robot_location[1] + direction[1])
                if position[0] < 0 or  position[0] >= len(self.huristic_map_) or position[1] < 0 or  position[1] >= len(self.huristic_map_[0]):
                    continue

                if last_move[0] + direction[0] == 0 and last_move[1] + direction[1] == 0:
                    continue

                if self.huristic_map_[position[0]][position[1]] < lowest_cost:
                    lowest_cost = self.huristic_map_[position[0]][position[1]]
                    best_move = direction

            next_estimate_robot_location = (estimate_robot_location[0] + best_move[0], estimate_robot_location[1] + best_move[1])
            self.huristic_map_[estimate_robot_location[0]][estimate_robot_location[1]] =  self.huristic_map_[next_estimate_robot_location[0]][next_estimate_robot_location[1]] + 1
            estimate_robot_location = next_estimate_robot_location
            last_move = best_move
            path.append(best_move)
        if (path == None):
            return []
        return path

    # A* : we don't have any information about map so we guess battry location
    # we choose the random location so that it is 
    def blind(self):
        # lets check it's not surrunded by the wall
        if self.battery_location_ != None and self.robot_location_ != self.battery_location_  :
            if self.is_there_any_posible_path(self.battery_location_):
                return self.manhattan()
            
        # find another dest randomly direct relationship to it's distance 
        
        else:
            y = self.robot_location_[0]
            x = self.robot_location_[1]
            manhattan_dis = []
            while self.visible_map_[y][x] != None:
                manhattan_dis = []
                for i in range(len(self.visible_map_)):
                    rows = []
                    for j in range(len(self.visible_map_[0])):
                        rows.append(abs(self.robot_location_[0] - i) + abs(self.robot_location_[1] - j))
                    manhattan_dis.append(rows)    
            
                manhattan_dis = np.array(manhattan_dis)
                linear_idx = np.random.choice(manhattan_dis.size, p=manhattan_dis.ravel()/float(manhattan_dis.sum()))
                x, y = np.unravel_index(linear_idx, manhattan_dis.shape)
                self.battery_location_ = (y, x)
            print ( " battry location is = " ,self.battery_location_)
            return self.manhattan()

    # bfs : h is equal to the blind
    # def bfs(self):
    #     for direction in self.posible_directions:
