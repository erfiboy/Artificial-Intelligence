import os
import cv2
import numpy as np
from os import listdir
from sklearn import metrics
import matplotlib.pyplot as plt
from os.path import isfile, join
from sklearn import svm
from sklearn.model_selection import cross_validate

directory = os.path.dirname(os.path.abspath(__file__))
print(directory)
mypath = directory + '\\images\\train' # edit with the path to your data
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

x_train = np.zeros([len(files), 256])
y_train = np.zeros([len(files), 1])

#loading train files
for index,file in enumerate(files):
    label = file.split('_')[0] 
    img = cv2.imread(mypath + "\\" + file, cv2.IMREAD_GRAYSCALE)
    img = np.reshape(img, [256, 1])
    x_train[index, :] = img.ravel()
    y_train[index] = int(label)

mypath = directory + '\\images\\test' # edit with the path to your data
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

x_test = np.zeros([len(files), 256])
y_test = np.zeros([len(files), 1])

#loading train files
for index,file in enumerate(files):
    label = file.split('_')[0] 
    img = cv2.imread(mypath + "\\" + file, cv2.IMREAD_GRAYSCALE)
    img = np.reshape(img, [256, 1])
    x_test[index, :] = img.ravel()
    y_test[index] = int(label)

number_of_folds = 10

kernel = "sigmoid"
coef0 = 5
trained_netwoek = svm.SVC(kernel=kernel, coef0 = coef0)

models = cross_validate(trained_netwoek, 
                        x_train, y_train.ravel(), 
                        cv = number_of_folds, 
                        return_estimator=True, 
                        n_jobs=5)

scores_of_folds = [ model.score(x_test,y_test.ravel()) for model in models['estimator'] ]

print("Maximum score in crossvalidation model is " + str(max(scores_of_folds)))
print("Avarage score in crossvalidation model is " + str(np.average(scores_of_folds)))
print("kernel = ", kernel, "coef0 =", coef0, "number_of_folds =", number_of_folds)
