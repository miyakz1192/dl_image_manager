#!/usr/bin/env python3

import keras.utils.image_utils as image
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import array_to_img
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("image_file", help="input image file",type=str)
args = parser.parse_args()

file = args.image_file

file_name = os.path.basename(file)
path_name = os.path.dirname(file)
#print(file_name)
#print(path_name)

org_img = image.load_img(file)
plt.imshow(org_img)
org_img = np.array(org_img)
print("org_img shape")
print(org_img.shape)

#矩形はりつけ
left_upper = org_img[0:400,0:400]
left_upper_img = array_to_img(left_upper, scale = False)
#plt.imshow(left_upper_img)
save_file_name_lu = path_name + "/" + "lu_" + file_name
image.save_img(save_file_name_lu, left_upper_img)

ymax = org_img.shape[0]
xmax = org_img.shape[1]
right_upper = org_img[0:400,xmax-400:xmax]
right_upper_img = array_to_img(right_upper, scale = False)
#plt.imshow(right_upper_img)
save_file_name_ru = path_name + "/" + "ru_" + file_name
image.save_img(save_file_name_ru, right_upper_img)


