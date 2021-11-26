import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib import interactive
import seaborn as sb
import time
import enum
import Astar as A
interactive(True)

class world():
    def __init__(self):
        self.WorldMap = self.ParseMap()
        self.show_map()
        print(self.WorldMap)
    
    def ParseMap(self):
        tree = ET.parse('SampleRoom.xml')
        rows = tree.findall('row')
        Map = []
        
        for row in rows:
            cells = []
            for cell in row:
                cells.append(cell.text)
            Map.append(cells)  
        return Map

    def celltype(self, cell):
        return self.WorldMap[cell[0]][cell[1]]

    def getrobotlocation(self):
        return self.getlocation('robot')
    
    def getbattrylocation(self):
        return self.getlocation('Battery')

    def getlocation(self, specifiedcell):
        for i, x in enumerate(self.WorldMap):    
            if specifiedcell in x:
                return (i, x.index(specifiedcell))

    def show_map(self):
        view_map = []
        for row in self.WorldMap:
            view_map_row = []
            for cell in row:
                if cell == "Battery":
                    view_map_row.append(2000)
                elif cell == "empty":
                    view_map_row.append(4000)
                elif cell == "obstacle":
                    view_map_row.append(-4000)
                elif cell == "robot":
                    view_map_row.append(-1000)
            view_map.append(view_map_row)

        ax = sb.heatmap(view_map, linewidths=1, linecolor='black', cmap='hot', cbar=False)
        ax.set(xticklabels=[], yticklabels=[])
        plt.ion()
        plt.show()
        plt.pause(1)
        
    def update_map(self, prev_robot_loc, next_robot_loc):
        self.WorldMap[prev_robot_loc[0]][prev_robot_loc[1]] = "empty"
        self.WorldMap[next_robot_loc[0]][next_robot_loc[1]] = "robot"
        self.show_map()

    def map_size(self):
        return len(self.WorldMap) , len(self.WorldMap[0])

class robot():
    def __init__(self, world, VisbleMap, destination, location, path, stepcount = 0) :
        self.world = world
        self.VisbleMap = VisbleMap
        self.destination = destination
        self.location = location
        self.path = path
        self.stepcount = stepcount

    def findpath(self):
        parh = A.manhattan(VisbleMap, location, destination)

    def battryfound(self):
        if (VisbleMap[location[0]][location[1]] == "Battery"):
            return True
        return False   

    def move(self):
        
        if (len(path) == 0):
            print("finding the new paht according to the new informations")
            return
        while(len(path) != 0):
            cell = (self.location[0] + path[0][0] , self.location[1] + path[0][1])
            targetcelltype = self.world.celltype(cell)
            path.pop(0)
            if (targetcelltype == "Battery"):
                self.world.update_map(self.location, cell)
                self.location = cell
                self.stepcount += 1
                print("battery found in ", self.stepcount , " steps!")
                return
            elif (targetcelltype == "empty"):
                self.world.update_map(self.location, cell)
                self.location = cell
                self.stepcount += 1
                self.VisbleMap[cell[0]][cell[1]] = "empty"
            elif (targetcelltype == "obstacle"):
                self.stepcount += 1
                self.VisbleMap[cell[0]][cell[1]] = "obstacle"
                findpath()



robot_world = world()
path = [(0,1),(1,0)]
y , x = robot_world.map_size()
visible_map = [[None for _ in range(x)] for _ in range(y)]
visible_map[robot_world.getrobotlocation()[0]][robot_world.getrobotlocation()[1]] = "empty"
robot = robot(robot_world, visible_map, None, robot_world.getrobotlocation(), path)
robot.move()
print ( robot_world.getrobotlocation())
print ( robot_world.getbattrylocation())