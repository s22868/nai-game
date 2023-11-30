"""
Authors: Mateusz Budzyński, Igor Gutowski

This script uses a Decision Tree Classifier to classify wine samples based on their alcohol and malic_acid content.

The dataset used is the wine dataset from scikit-learn, containing samples from three different classes.

The Decision Tree model is trained and evaluated on both the training and test sets. Classification reports are printed for both sets.
"""
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier

from utils.visualize_classifier import visualize_classifier

from sklearn import datasets

#load dataset

wine = datasets.load_wine()

#x - data (alcohol, malic_acid) y - target (class ---- 0, 1, 2)
X = wine.data[:, :2]
y = wine.target

#split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

#train model
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

#generate report
print("TRAIN")
print(classification_report(y_train, clf.predict(X_train)))
print("TEST")
print(classification_report(y_test, y_pred))

visualize_classifier(clf, X_train, y_train, "TRAIN")

visualize_classifier(clf, X_test, y_test, "TEST")
