#!/usr/bin/env python3

#starndard lib
import subprocess
import argparse
import glob
import os
import shutil
import sys
import re

#my lib
sys.path.append("./lib/")
from get_current_process_user_home_dir import *
from dl_image_manager_constants import *
from build_lib import *
import gaa_lib_loader
import gaa_constants
from easy_sshscp import *


class AutoProject:
    def __init__(self):
        self.home_dir = get_current_process_user_home_dir()

        self.prefix = "autogenclose_"
        self.prefix_r = r'.*/autogenclose_*'
        self.additional_merge_target_src_prj = []
        self.additional_merge_target_src_prj_file_path = self.home_dir + DL_IMAGE_MANAGER_CONFIG_DIR + DL_IMAGE_MANAGER_ADDITIONAL_MERGE_TARGET_SRC_PRJ_FILE_NAME

    def __download_images(self):
        ssh = EasySSHSCP()
        host = "scrcpy"
        cmd = "tar cvfz /tmp/images.tar.gz -C %s %s" % (gaa_constants.GAA_HOME_DIR , gaa_constants.GAA_AUTO_GEN_DIR)
        ssh.ssh(host, cmd)
        ssh.download(host, "/tmp/images.tar.gz", "./images.tar.gz")
        subprocess.run(["tar", "xvfz", "./images.tar.gz"])

    def __save_additional_merge_target_src_prj_file(self):
        #give shot name
        fname = self.additional_merge_target_src_prj_file_path
        with open(fname, mode="w") as f:
            f.write("\n".join(self.additional_merge_target_src_prj))

    def __check_already_created_in_projects(self):
        dirname = self.home_dir + DL_IMAGE_MANAGER_PROJECTS
        targets = glob.glob(dirname + "/*")

        for i in targets:
            if re.match(self.prefix_r, i) is not None:
                print("ERROR: already created in projects %s" % i)
                raise ValueError()

    def __get_next_index(self):
        pass

    def __create_hash_db(self):
        pass

    def __check_hash_db(self):
        pass

    def __get_checksum(self, image_file):
        pass

    def __is_already_added(self, target_image_file):
        s = self.__get_checksum(target_image_file)
        return self.__check_hash_db(s)

    def __make_project(self, new_prj_name, master_image_file):
        #TODO:do make_project.sh newname with master image 
        #TODO: do gen_anno_xml.py
        pass

    def __get_image_file_list(self, target_prj, kind):
        pass

    def create_project(self):
        target_prj = "close"

        self.__download_images()
        self.__check_already_created_in_projects()
        next_idx = self.__get_next_index()

        targets = self.__get_image_file_list(target_prj, "true")

        for t in targets:
            if self.__is_already_added(t) is True:
                continue

            new_prj_name = self.prefix + str(next_idx)
            self.__make_project(new_prj_name, t)
            self.additional_merge_target_src_prj.append(new_prj_name)
            next_idx += 1

        self.__save_additional_merge_target_src_prj_file()

if __name__ == "__main__":
    ap = AutoProject()
    ap.create_project()


