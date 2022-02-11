from concurrent.futures import thread
import os
import cv2
import random
import numpy as np
from os import listdir
from os.path import isfile, join
from copy import deepcopy
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPRegressor

def flip_color(pixel):
    if pixel > 128:
        return random.randint(0,128)
    else:
        return random.randint(128,255)

def add_noise_to_picture(images,threshold):
    for image in images:
        choosen_pixels = random.sample(range(1, 255), 50)
        for pixel in choosen_pixels:
            if (random.randint(1,100) > threshold):
                image[pixel] = flip_color(image[pixel])
    return images


directory = os.path.dirname(os.path.abspath(__file__))
print(directory)
mypath = directory + '\\images\\train' # edit with the path to your data
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

original_images_train = np.zeros([len(files), 256])
y_train = np.zeros([len(files), 1])

#loading train files
for index,file in enumerate(files):
    label = file.split('_')[0] 
    img = cv2.imread(mypath + "\\" + file, cv2.IMREAD_GRAYSCALE)
    img = np.reshape(img, [256, 1])
    original_images_train[index, :] = img.ravel()
    y_train[index] = int(label)

mypath = directory + '\\images\\test' # edit with the path to your data
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

original_images_test = np.zeros([len(files), 256])
y_test = np.zeros([len(files), 1])

#loading train files
for index,file in enumerate(files):
    label = file.split('_')[0] 
    img = cv2.imread(mypath + "\\" + file, cv2.IMREAD_GRAYSCALE)
    img = np.reshape(img, [256, 1])
    original_images_test[index, :] = img.ravel()
    y_test[index] = int(label)


threshold = 25
noisy_images_train = add_noise_to_picture(deepcopy(original_images_train), threshold)
noisy_images_test = add_noise_to_picture(deepcopy(original_images_test), threshold)

number_of_iteration = 1000
hidden_layer = (1000, 1000)

trained_netwoek = MLPRegressor( hidden_layer_sizes= hidden_layer,
                                max_iter=number_of_iteration,
                                random_state=1,
                                shuffle=True).fit(noisy_images_train, original_images_train)

accuracy = trained_netwoek.score(noisy_images_test, original_images_test)
print(" accuracy = ", accuracy )
estimated_images_test = trained_netwoek.predict(noisy_images_test)
save_path = directory + "\\hard_noise1000_" + str(threshold) + "_" +str(50) + "_acc =" +str(accuracy)
os.mkdir(save_path)

for i in range(1,20):
    original = np.reshape(original_images_test[i * 100, :], [16, 16])
    estimated = np.reshape(estimated_images_test[i * 100, :], [16, 16])
    noisy = np.reshape(noisy_images_test[i * 100, :], [16, 16])
    cv2.imwrite(save_path+ "\\" +str(i)+'_original.png', original)
    cv2.imwrite(save_path+ "\\" +str(i)+'_estimated.png', estimated)
    cv2.imwrite(save_path+ "\\" +str(i)+'_noisy.png', noisy)
