import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm


n_samples = 500
xx, yy = np.meshgrid(np.linspace(-10, 10, 500), np.linspace(-10, 10, 500))
np.random.seed(0)
X = np.random.randn(500, 2)
Y = np.logical_xor(X[:, 0] > 0, X[:, 1] > 0)



kernel = "sigmoid"

coef0 = 4
# fit the model
clf = svm.SVC(kernel=kernel, coef0 = coef0)
clf.fit(X, Y)

# plot the decision function for each datapoint on the grid
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.imshow(
    Z,
    interpolation="nearest",
    extent=(xx.min(), xx.max(), yy.min(), yy.max()),
    aspect="auto",
    origin="lower",
    cmap=plt.cm.coolwarm,
    alpha = 0.3
)
contours = plt.contour(xx, yy, Z, levels=[0], linewidths=2, linestyles="dashed")
plt.scatter(X[:, 0], X[:, 1], s=30, c=Y, cmap=plt.cm.coolwarm, edgecolors="k")
plt.xticks(())
plt.yticks(())
plt.axis([-3, 3, -3, 3])

directory = os.path.dirname(os.path.abspath(__file__))

name = "\\kernel_" + str(kernel) +  "_samples_" + str(n_samples)  \
                    + "_coef0_" + str(coef0) + ".png"

save_path = directory + "\\results" + name
print(save_path)
plt.savefig(save_path)
plt.show()