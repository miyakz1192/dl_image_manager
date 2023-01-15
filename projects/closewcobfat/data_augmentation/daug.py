#!/usr/bin/env python3
import sys
sys.path.append("./lib/")

from get_current_process_user_home_dir import *
from data_aug import *
from dl_image_manager_constants import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("project_name", type=str)
args = parser.parse_args()

home_dir = get_current_process_user_home_dir()

project_name = args.project_name

image_file_path = home_dir + DL_IMAGE_MANAGER_PROJECTS_MASTER_IMAGE %(project_name)
save_file_path = home_dir + DL_IMAGE_MANAGER_PROJECTS_BUILD %(project_name)
gen = DataAugmentationGenerator(image_file_path=image_file_path, save_dir=save_file_path, save_file_prefix=project_name,cval=255)

#gen.suite()
gen.mix()
