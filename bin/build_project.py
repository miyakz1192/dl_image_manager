#!/usr/bin/env python3

import sys
sys.path.append("./lib/")

from get_current_process_user_home_dir import *
from dl_image_manager_constants import *
from xml_lib import * 

import argparse
import subprocess
import glob
import os

parser = argparse.ArgumentParser()
parser.add_argument("project_name", type=str)
args = parser.parse_args()

home_dir = get_current_process_user_home_dir()
project_name = args.project_name

command = [home_dir + DL_IMAGE_MANAGER_PROJECTS_DATAAUG_BIN % (project_name), project_name]


print("INFO: bulding project of %s" % (project_name))
print("INFO: executing projects daug.py")

res = subprocess.run(command, capture_output=True, text=True).stdout
print(res)

build_file_path = home_dir + DL_IMAGE_MANAGER_PROJECTS_BUILD % (project_name)

files = glob.glob(build_file_path + "/*")

xmlo = XMLOperator()
xmlo.read(home_dir + DL_IMAGE_MANAGER_PROJECTS_MASTER_XML % (project_name))

for one_file in files:
    xmlo.rewrite("filename", os.path.basename(one_file))

    dir_name = os.path.dirname(one_file)
    basename = os.path.basename(one_file)

    file_name = os.path.splitext(basename)[0]
    ext_name  = os.path.splitext(basename)[1]

    output_file_name = dir_name + "/" + file_name + ".xml"

    xmlo.write(output_file_name)
