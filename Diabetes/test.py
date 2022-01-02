import numpy as np

x = np.random.randint(low=25, high=200, size=10)

x = np.sort(x)

print(x)

for i in range(len(x)):
    g = np.digitize(x, bins=[50,100])
    
print(g)