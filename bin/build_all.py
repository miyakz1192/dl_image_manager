#!/usr/bin/env python3

import sys
sys.path.append("./lib/")

from get_current_process_user_home_dir import *
from dl_image_manager_constants import *

import subprocess
import glob
import os

home_dir = get_current_process_user_home_dir()

project_dirs = glob.glob(home_dir + DL_IMAGE_MANAGER_PROJECTS + "/*")

for project_dir in project_dirs:
    project_name = os.path.basename(project_dir)
    print("INFO: building %s" % project_name)

    command = [home_dir + DL_IMAGE_MANAGER_BUILD_PROJECT_BIN, project_name] 
    #res = subprocess.run(command, capture_output=True, text=True).stdout
    res = subprocess.check_output(command)
    print(res)

