"""
Authors: Mateusz Budzyński, Igor Gutowski

This script uses a Support Vector Machine (SVM) to classify wine samples based on their alcohol and malic_acid content.

The dataset used is the wine dataset from scikit-learn, containing samples from three different classes.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets

# load dataset
wine = datasets.load_wine()

# x - data (alcohol, malic_acid) y - target (class ---- 0, 1, 2)
X = wine.data[:, :2]
y = wine.target

# train model
C = 1.0
svc = svm.SVC(kernel="linear", C=C).fit(X, y)


markers = ("o", "x", "s")

x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1

x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1

res = (x1_max / x1_min) / 100

# create a mesh
xx1, xx2 = np.meshgrid(
    np.arange(x1_min, x1_max, res), np.arange(x2_min, x2_max, res)
)
Z = svc.predict(np.c_[xx1.ravel(), xx2.ravel()])
Z = Z.reshape(xx1.shape)

# generate plot
plt.contourf(xx1, xx2, Z, alpha=0.4)

plt.xlim(xx1.min(), xx1.max())

plt.ylim(xx2.min(), xx2.max())

for idx, cl in enumerate(np.unique(y)):
    plt.scatter(
        x=X[y == cl, 0],
        y=X[y == cl, 1],
        alpha=0.8,
        marker=markers[idx],
        label=cl,
    )

plt.xlabel("alcohol")

plt.ylabel("malic_acid")

plt.legend(loc="upper left")

plt.show()
