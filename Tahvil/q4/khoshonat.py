import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

x = np.array([120, 121, 122, 123, 124, 125, 126, 130, 133, 131, 130, 143, 149, 153, 155, 157, 160, 164, 173, 178, 191, 164, 199, 202, 213, 
            220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360 , 370, 380, 390, 400, 410, 420, 430, 440, 450, 
            460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 593, 601, 610, 625, 630, 640, 650, 660, 670, 680,
            690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920,
             930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030])
y = np.array([255, 253, 249 ,243, 239, 235, 223, 210, 208, 205 ,203, 196, 184, 191, 184, 180, 170, 170, 170, 170, 164, 158, 156, 164, 149,
            145, 146, 124, 111, 102, 90, 80, 80, 77, 70, 66, 66, 69, 67, 67, 77, 77, 85, 87, 89, 85, 81, 82, 81, 90, 98,
             98, 107, 112, 120, 114, 111, 114, 111, 114,  111, 110, 108, 98, 99, 109, 117, 114, 114, 114, 114, 114, 114, 114, 114,
              114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114,  114, 114, 114, 114, 114, 114, 114, 114, 114, 114,
              114, 114, 114, 114, 114, 114, 114, 114, 122, 125])

y = np.array([ (640 - i)-385 for i in y])
x_train = []
x_test = []
y_train = []
y_test = []

for i in range(len(x)):
    if i % 7 == 0:
        x_test.append(x[i])
        y_test.append(y[i])
    else:
        x_train.append(x[i])
        y_train.append(y[i])

x_train = np.array(x_train).reshape(-1,1)
x_test = np.array(x_test).reshape(-1,1)
y_train = np.array(y_train).reshape(-1,1)
y_test = np.array(y_test).reshape(-1,1)

# x_train = x_train.reshape(-1,1)
# x_test = x_test.reshape(-1,1)

number_of_iteration = 1000
hidden_layer = [10,10]
trained_netwoek = MLPRegressor( hidden_layer_sizes= hidden_layer,
                                max_iter=number_of_iteration,
                                solver = 'lbfgs',
                                activation='logistic',
                                alpha= 1e-10,
                                random_state=1,
                                shuffle=True).fit(x_train, y_train.ravel())

y_result = trained_netwoek.predict(x_test)

error = mean_squared_error(y_result, y_test)

fig, ax = plt.subplots()
train_plt, = plt.plot(x_train, y_train, label='Train',  linewidth=3, linestyle=':')
test_plt,  = plt.plot(x_test, y_result, label='Test')
expected_plt,  = plt.plot(x_test, y_test, label='Expected_result', linestyle='--')
ax.set_title('Mean squared error: ' + str(round(error,3)))
ax.legend(handles=[train_plt, test_plt, expected_plt])
name = "linear_1-7" + str(number_of_iteration) + "_" + str(hidden_layer) + '.png'
plt.savefig(name)
plt.show()