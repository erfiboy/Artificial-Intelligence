Find the battery
Problem: There is a robot which is located in an unknown place.The robot's battery is low so it's searching for a battery that knows it would be some where in the map but it doesn't have any infromation about where the battery is and there are some obstacles in it's path that's impossible to pass through them.The problem is to find a path to from robot to the battery.
Solution: First of all we don't have any information about the map so we should explore the map inorder to find the path.
Now lets break a problem to simpler problem:
Knowing battery location:
With konwing the battry loaction our algorithm has three phase.

forward phase:
We can choose our huristic the direct distance between to any cell of our map to the battry.
For example if the battery is in (2,1) and (5,5) is our target the cost is qual to:
sqrt( (5-2)^2 + (5-1)^2) = 5
backward correction:

After calculationg the huristic for the first time we should update the matrix with our information which we have gained in our exploration. We do this by updating the cost of cells we just visited.
For ecample: consider the following map and assume that we are in the center of the map (cell with value equal to 2.5) and the numbers in the map are the huristic that we calculated in the last phase:
5	4	3
4	2.5	2.1
3.2	3	2.9
so we will choose the adjusent cell with the lowest value which in this case is equal to 2.1. after choosing 2.1 we update the 2.5 to 2.1 + 1 where 1 is the cost to go to the next cell. And the current cell is 2.1.

5	4	3
4	3.1	2.1
3.2	3	2.9
Those who cannot remember the past are condemned to repeat it:

In order to not search a repetitive cell and not stack in a loop we get the matrix from the robot every time the robot calls find path and run the algorithm. For example if robot passes the (x,y) cells to time the value of coresponding [x][y] cell in the matrix sets to 2. And in calculating the huristic value we multiply the value of this value to a constant and add it with the cost of huristic to set higher value for the unexplored cells.