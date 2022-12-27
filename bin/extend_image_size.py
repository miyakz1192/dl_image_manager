#!/usr/bin/env python3

import keras.utils.image_utils as image
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.utils import array_to_img
import argparse
import os

import sys
sys.path.append("./lib/")
from get_current_process_user_home_dir import *
from dl_image_manager_constants import *
home_dir = get_current_process_user_home_dir()

import pdb

#全体的な作戦としては、numpyのarray(2次元)を適当に作ってやって、それをimgに変換して、save_imgで書きだしてやれば完了な気がする。
#あとは、以下のURLにやり方が書いてあるが、400 x 400の画像に32 x 32のcloseを貼り付ければ良いだけ。
#https://note.nkmk.me/python-numpy-image-processing/


#bug
#--output_size shuold not be used. TODO:

DEFAULT_OUTPUT_SIZE = (400,400)
DEFAULT_COLOR = 255

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("project_name", type=str)
    parser.add_argument("target_image", type=str)
    parser.add_argument("--output_size", help="optional output size(widthxheight) like 400x400")
    parser.add_argument("--color", help="color like 255(unsigned char)", default=DEFAULT_COLOR)
    parser.add_argument("--output_file", help="output file name")

    args = parser.parse_args()
    return(args)

def output_size(args):
    print("user input output_size = %s" % (args.output_size))

    if args.output_size is None:
        print("set default size = %s" % (str(DEFAULT_OUTPUT_SIZE)))
        return DEFAULT_OUTPUT_SIZE
    else:
        temp = args.output_size.split("x")
        return (int(temp[0]), int(temp[1]))

def output_file(args):
    if args.output_file is not None:
        return

    print("set default output_file")
    return home_dir + DL_IMAGE_MANAGER_PROJECTS_MASTER_EXTENDED_IMAGE % (args.project_name)



def check_image_size(target_image, output_size):
    tx = target_image.shape[0]
    ty = target_image.shape[1]

    ox = output_size[0]
    oy = output_size[1]

    if not (ox >= tx and oy >= ty):
        print("ERROR: output_size must be larger than target_size")
        raise ValueError("output_size must be larger than target_size")

    return True

def main():
    args = get_args()
    o_size = output_size(args)
    o_file_name = output_file(args)
    print("determined output_size = %s" % (str(o_size)))
    print("determined output_file = %s" % (o_file_name))

    print("loading input image")
    target_image = image.load_img(args.target_image)
    #画像をnumpy配列に変換する
    target_image = np.array(target_image)
    print("target_image shape=%s" %(str(target_image.shape)))

    check_image_size(target_image, o_size)

    print("make backimage")
    plt.figure(figsize = (1, 1))
    back_image = np.full((o_size[0], o_size[1],3), 255)
    print(back_image.shape)
    
    #矩形はりつけ
    tx = target_image.shape[0]
    ty = target_image.shape[1]
    back_image[0:tx,0:ty] = target_image[0:tx,0:ty]
    save_img = array_to_img(back_image, scale = False)
    image.save_img(o_file_name, save_img)

    print("done")


if __name__ == '__main__':
    main()
