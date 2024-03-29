import os
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def linear(domain):
    result = []
    for i in domain:
        result.append([(i[0]+i[1]) , (i[0]-i[1])])
    return result

# Test for the EASY function
random.seed(1)

train_domain_x = (-50, 50)
train_domain_y = (150, 200)
x_train = np.transpose(np.array([np.linspace(train_domain_x[0], train_domain_x[1], 100),np.linspace(train_domain_y[0], train_domain_y[1], 100)]))
z_train = np.array(linear(x_train))

test_domain_x = (-150, 150)
test_domain_y = (100, 250)
x_test = np.transpose(np.array([np.linspace(test_domain_x[0], test_domain_x[1], 200),np.linspace(test_domain_y[0], test_domain_y[1], 200)]))
z_test= np.array(linear(x_test))

number_of_iteration = 1000
best_error = 1e20
best_result = None
best_network = None
best_hidden_layer = None
for i in range(10,20):
    for j in range(10,20):
        for k in range(10,20):
            hidden_layer = (i,j,k)
            trained_netwoek = MLPRegressor( hidden_layer_sizes= hidden_layer,
                                            max_iter=number_of_iteration,
                                            random_state=1,
                                            shuffle=True).fit(x_train, z_train)
            z_result =  np.array(trained_netwoek.predict(x_test))
            error = mean_squared_error(z_result, z_test)
            if (best_error > error):
                best_error = error
                best_hidden_layer = hidden_layer
                best_network = trained_netwoek

clearConsole()
print('MSE:'+str(best_error), "in network with hidden layer equals to: " , str(best_hidden_layer))
