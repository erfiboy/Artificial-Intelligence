import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import seaborn as sb
import time
from Algorithm import Algorithm

class world():
    def __init__(self):
        self.WorldMap = self.ParseMap()
        self.show_map()
    
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
        if cell[0] < 0 or cell[1] < 0 or cell[0] >= len(self.WorldMap) or cell[1] >= len(self.WorldMap[0]) :
            return "obstacle"
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
    def __init__(self, world, visbleMap, destination, location, path, stepcount = 0):
        self.path = path
        self.world = world
        self.location = location
        self.visbleMap = visbleMap
        self.stepcount = stepcount
        self.destination = destination
        self.alogorithm_ = Algorithm(visbleMap, location, destination)

    def findpath(self):
        self.alogorithm_.set_map(self.visbleMap)
        self.alogorithm_.set_robot_location(self.location)
        self.path = self.alogorithm_.exec()

    def battryfound(self):
        if (visbleMap[location[0]][location[1]] == "Battery"):
            return True
        return False   

    def move(self):
        while(True):

            while len(self.path) == 0:
                print("finding the new path according to the new informations")
                self.findpath()

            cell = (self.location[0] + self.path[0][0] , self.location[1] + self.path[0][1])
            targetcelltype = self.world.celltype(cell)
            self.path.pop(0)
            
            if targetcelltype == "Battery":
                self.world.update_map(self.location, cell)
                self.location = cell
                self.stepcount += 1
                print("battery found in ", self.stepcount , " steps!")
                return
            elif targetcelltype == "empty":
                self.world.update_map(self.location, cell)
                self.location = cell
                self.stepcount += 1
                self.visbleMap[cell[0]][cell[1]] = "empty"
            elif targetcelltype == "obstacle":
                self.stepcount += 1
                self.visbleMap[cell[0]][cell[1]] = "obstacle"
                self.findpath()



robot_world = world()
y , x = robot_world.map_size()
visible_map = [[None for _ in range(x)] for _ in range(y)]
visible_map[robot_world.getrobotlocation()[0]][robot_world.getrobotlocation()[1]] = "empty"
robot = robot(robot_world, visible_map,  robot_world.getbattrylocation(), robot_world.getrobotlocation(), [])
robot.move()
