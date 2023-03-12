#!/usr/bin/env python3

import cv2
import os
import argparse
import sys
import shutil

sys.path.append("./lib/")
from get_current_process_user_home_dir import *
from dl_image_manager_constants import *
from xml_lib import * 

parser = argparse.ArgumentParser()
parser.add_argument("project_name", help="project name of auto creation annotation xml target", type=str)
args = parser.parse_args()

home_dir = get_current_process_user_home_dir()

master_image_path = home_dir + DL_IMAGE_MANAGER_PROJECTS_MASTER_IMAGE % (args.project_name)

master_xml_path = home_dir + DL_IMAGE_MANAGER_PROJECTS_MASTER_XML % (args.project_name)

sample_master_xml_path = home_dir + DL_IMAGE_MANAGER_SAMPLE_MASTER_XML

if os.path.exists(master_image_path) is False:
    print("ERROR: %s is not found." % master_image_path)

img = cv2.imread(master_image_path)
height = img.shape[0]
width  = img.shape[1]

print("INFO: image size w=%d, h=%d" % (width, height))
print("INFO: copy sample master xml")
shutil.copyfile(sample_master_xml_path, master_xml_path)
print("INFO: rewrite xml")

height = str(height)
width = str(width)

xmlo = XMLOperator()
xmlo.read(master_xml_path)
xmlo.rewrite("name", args.project_name)
xmlo.rewrite("width", width)
xmlo.rewrite("height", height)
xmlo.rewrite("xmax", width)
xmlo.rewrite("ymax", height)
xmlo.write(master_xml_path)
