import sys

#for CLI environment
sys.path.append("./lib/")
#for jupyter environment
sys.path.append("../../../lib/")

from get_current_process_user_home_dir import *
from data_aug import *

home_dir = get_current_process_user_home_dir()

image_file_path = home_dir + "/dl_image_manager/projects/close/master/image.jpg"
gen = DataAugmentationGenerator(image_file_path=image_file_path, save_dir="/tmp/")

gen.suite()
