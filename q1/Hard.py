import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor

def exponential(domain):
    result = [ math.sin(2*math.pi*i) + math.sin(5*math.pi*i) for i in domain]
    return result

def calculate_error(estimated, goal):
    return np.sum((estimated-goal)**2)**0.5/len(estimated)

# Test for the EASY function
points = 7000
train_domain = (-4, 4)
x_train = np.linspace(train_domain[0], train_domain[1], points).reshape(-1, 1)
y_train = np.array(exponential(x_train)).reshape(-1, 1)

test_domain = (-4, 4)
x_test = np.linspace(test_domain[0], test_domain[1], 8000).reshape(-1, 1)
y_test = np.array(exponential(x_test)).reshape(-1, 1)

number_of_iteration = 400
hidden_layer = (20,40,50,30)
trained_netwoek = MLPRegressor( hidden_layer_sizes= hidden_layer,
                                max_iter=number_of_iteration,
                                random_state=1,
                                shuffle=True).fit(x_train, y_train.ravel())

y_result = trained_netwoek.predict(x_test)

error = calculate_error(y_result, y_test)

fig, ax = plt.subplots()
train_plt, = plt.plot(x_train, y_train, label='Train',  linewidth=3, linestyle=':')
test_plt,  = plt.plot(x_test, y_result, label='Test')
expected_plt,  = plt.plot(x_test, y_test, label='Expected_result')
ax.set_title('Mean squared error: ' + str(round(error,3)))
ax.legend(handles=[train_plt, test_plt, expected_plt])
name = "exponential_" + str(points) + '.png'
plt.savefig(name)
plt.show()