#!/usr/bin/env python3

import sys
sys.path.append("./lib/")

from get_current_process_user_home_dir import *
from dl_image_manager_constants import *
from build_lib import *

import subprocess
import argparse
import glob
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--train_percent", help="data size of train by percent", default=80, type=int)
parser.add_argument("--data_format", help="data format of specific DL implementation. ex: pytorch", default="pytorch", type=str)
args = parser.parse_args()

home_dir = get_current_process_user_home_dir()

project_dirs = glob.glob(home_dir + DL_IMAGE_MANAGER_PROJECTS + "/*")

def check_data_format(args):
    if args.data_format != "pytorch":
        raise ValueError("ERROR: invalid data format")

check_data_format(args)

data_set = {}

print("INFO: building train_set and valid_set")
for project_dir in project_dirs:
    project_name = os.path.basename(project_dir)
    project_build_dir = home_dir + DL_IMAGE_MANAGER_PROJECTS_BUILD % (project_name)
    print("INFO: building data set about %s" % project_name)
    res = make_train_valid_data(project_build_dir, args.train_percent)

    data_set[project_name] = res
   
    #TRACE INFO
    train_set = res[0]
    valid_set = res[1]
    print("  TRACE:train_set.size == %d" %(len(train_set)))
    print("  TRACE:valid_set.size == %d" %(len(valid_set)))


#TODO: be classes and using strategy pattern
print("INFO: building data set format for pytorch")
print("INFO: clean up data_set dir")

data_set_dir = "./data_set"
ANNOTATIONS = "Annotations"
IMAGE_SETS  = "ImageSets"
IMAGE_SETS_MAIN = "Main"
JPEG_IMAGES = "JPEGImages"
TRAIN_FILE = "train.txt"
TRAIN_VAL_FILE = "trainval.txt"
TEST_FILE = "test.txt"
VAL_FILE = "val.txt"
data_set_sub_dir = [ANNOTATIONS, IMAGE_SETS, JPEG_IMAGES]

if(os.path.isdir(data_set_dir) == True):
    shutil.rmtree(data_set_dir)
    os.makedirs(data_set_dir)

for d in data_set_sub_dir:
    os.makedirs(data_set_dir + "/" + d)


os.makedirs(data_set_dir + "/" + IMAGE_SETS + "/" + "Main")

print("INFO: copy annotation jpg/xml file")
for project_dir in project_dirs:
    project_name = os.path.basename(project_dir)
    train_set = data_set[project_name][0] 
    valid_set = data_set[project_name][1] 

    build_dir = home_dir + DL_IMAGE_MANAGER_PROJECTS_BUILD % (project_name)

    jpg_files = train_set + valid_set
    annotations = list(map(lambda x: change_file_ext(x, ".xml") , jpg_files))

    for anno_file in annotations:
        command = ["cp", build_dir + "/" + anno_file, data_set_dir + "/" + ANNOTATIONS]
        subprocess.call(command)

    for jpg_file in jpg_files:
        command = ["cp", build_dir + "/" + jpg_file, data_set_dir + "/" + JPEG_IMAGES]
        subprocess.call(command)

train_file = data_set_dir + "/" + IMAGE_SETS + "/" + IMAGE_SETS_MAIN + "/" + TRAIN_FILE
val_file = data_set_dir + "/" + IMAGE_SETS + "/" + IMAGE_SETS_MAIN + "/" + VAL_FILE

print("INFO: build files")
for project_name, train_val in data_set.items():
    print("project %s" % project_name)
    train_set = train_val[0]
    valid_set = train_val[1]
    print("======train====== %d" % (len(train_set)))
    for i in train_set:
        with open(train_file, "a") as f:
            f.write(i+"\n")
    print("=====val====== %d" % len(valid_set))
    for i in valid_set:
        with open(val_file, "a") as f:
            f.write(i+"\n")

train_val_file = data_set_dir + "/" + IMAGE_SETS + "/" + IMAGE_SETS_MAIN + "/" + TRAIN_VAL_FILE
test_file = data_set_dir + "/" + IMAGE_SETS + "/" + IMAGE_SETS_MAIN + "/" + TEST_FILE

command = ["cp", val_file, train_val_file]
subprocess.call(command)
command = ["cp", val_file, test_file]
subprocess.call(command)

command = ["tar", "cvfz", "data_set.tar.gz", data_set_dir]
subprocess.call(command)

