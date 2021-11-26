import sys

class Algorithm():

    def __init__(self ,visible_map, robot_location, battery_location):
        self.method_ = "manhattan"
        self.visible_map_ = visible_map
        self.robot_location_ = robot_location
        self.battery_location_ = battery_location
        self.posible_directions = [(0,1),(1,0),(-1,0),(0,-1)]

    def update(self, method, visible_map, robot_location, battery_location):
        self.method_ = method
        self.visible_map_ = visible_map
        self.robot_location_ = robot_location
        self.battery_location_ = battery_location

    def set_map(self, visible_map):
        self.visible_map_ = visible_map
        
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
        elif self.method_ == "dfs":
            return self.dfs()

    # A* : h is equal to the manhattan distance between battry and robot
    def manhattan(self):
        path = []
        estimate_robot_location = self.robot_location_
        last_move = (0,0)
        while(self.battery_location_ != estimate_robot_location):
            best_move = (0,0)
            lowest_cost = 1e15
            for direction in self.posible_directions:
                position = (estimate_robot_location[0] + direction[0], estimate_robot_location[1] + direction[1])
                if position[0] >= len(self.visible_map_) or position[1] >= len(self.visible_map_[0]):
                    continue
                if  self.visible_map_[position[0]][position[1]] == "obstacle" or (last_move[0] + direction[0], last_move[1] + direction[1]) == (0,0) :
                    continue

                h = abs(self.battery_location_[0] - position[0]) + abs(self.battery_location_[1] - position[1])
                g = abs(self.robot_location_[0] - position[0]) + abs(self.robot_location_[1] - position[1])
                f = h + g

                if lowest_cost > (f):
                    best_move = direction
                    lowest_cost = f

            estimate_robot_location = (estimate_robot_location[0] + best_move[0], estimate_robot_location[1] + best_move[1])        
            last_move = best_move
            path.append(best_move)

        return path

    # A* : h is equal to the blind
    def blind():
        print("blind")

    # dfs : h is equal to the blind
    def dfs(self):
        print("salam")