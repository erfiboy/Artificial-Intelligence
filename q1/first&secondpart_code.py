import os
import numpy as np
from sklearn import svm
from sklearn.datasets import make_blobs, make_circles, make_multilabel_classification
import matplotlib.pyplot as plt

n_samples = 500
cluster_std = 0.2
X, y = make_blobs(n_samples=n_samples, centers=2,
                  random_state=0, cluster_std= cluster_std)

# c = 100
kernel = "linear"
C = 1
clf = svm.SVC(kernel=kernel,  C = C)
clf.fit(X, y)

plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)

ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

ax.contour(
    XX, YY, Z, colors="k", levels=[-1, 0, 1], alpha=0.5, linestyles=["--", "-", "--"]
)
ax.scatter(
    clf.support_vectors_[:, 0],
    clf.support_vectors_[:, 1],
    s=100,
    linewidth=1,
    facecolors="none",
    edgecolors="k",
)

ax.set_title('SVM classification')

directory = os.path.dirname(os.path.abspath(__file__))

name = "\\kernel_" + str(kernel) +  "_samples_" + str(n_samples) + "_cluster_std_" \
                    + str(cluster_std) + "_C_" + str(C) + ".png"

save_path = directory + "\\results" + name
print(save_path)
plt.savefig(save_path)
plt.show()